package controllers

import (
	"context"
	"io"
	"net/http"
	"regexp"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"github.com/siamliam12/coffee_store/models"
	"github.com/siamliam12/coffee_store/responses"
	"github.com/siamliam12/coffee_store/utils"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/gridfs"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var coffeeCollection *mongo.Collection = utils.GetCollection(utils.DB, "coffee") //coming for models to collect the collection from db
var validate = validator.New()                                                   //validator libary

// function to create a coffee in a database
func CreateCoffee(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var coffee models.Coffee
	defer cancel()

	//check if file is present in request body or not
	fileHeader, err := c.FormFile("image")
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}

	//check if file is of type image or not
	fileExtension := regexp.MustCompile(`\.[a-zA-Z0-9]+$`).FindString(fileHeader.Filename)
	if fileExtension != ".jpg" && fileExtension != ".jpeg" && fileExtension != ".png" {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{
			"error": true,
			"msg":   "Invalid file type",
		})
	}

	//read file content
	file, err := fileHeader.Open()
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}
	content, err := io.ReadAll(file)
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}

	//validate the request body
	if err := c.BodyParser(&coffee); err != nil {
		//get the error message the response template
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}
	//USE the validator library to validate required fields
	if validationErr := validate.Struct(&coffee); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}
	// Create db connection
	db := utils.ConnectDB().Database("cafe")

	//create bucket
	opts := options.GridFSBucket().SetName("images")
	bucket, err := gridfs.NewBucket(db, opts)

	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": true,
			"msg": err.Error(),
		})
	}
	// Upload file to GridFS bucket
	uploadStream, err := bucket.OpenUploadStream(fileHeader.Filename, options.GridFSUpload().SetMetadata(fiber.Map{"ext": fileExtension}))
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}

	//close upload stream
	fieldId := uploadStream.FileID
	defer uploadStream.Close()

	//write file content to upload stream
	filesize, err := uploadStream.Write(content)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}

	newCoffee := models.Coffee{
		Id:          primitive.NewObjectID(),
		Name:        coffee.Name,
		Price:       coffee.Price,
		Description: coffee.Description,
		Sizes:       coffee.Sizes,
		Category:    coffee.Category,
		Flavour:     coffee.Flavour,
		ImageFileID: fieldId.(primitive.ObjectID),
	}
	result, err := coffeeCollection.InsertOne(ctx, newCoffee)
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}
	return c.Status(http.StatusCreated).JSON(responses.CoffeeResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result,
		"msg": "Image uploaded successfully",
		"image": fiber.Map{
			"id":   fieldId,
			"name": fileHeader.Filename,
			"size": filesize,
		}}})
}

func GetACoffee(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Second)
	coffeeId := c.Params("coffeeId")
	var coffee models.Coffee
	defer cancel()

	//get coffee data
	objId, _ := primitive.ObjectIDFromHex(coffeeId)
	err := coffeeCollection.FindOne(ctx, bson.M{"id": objId}).Decode(&coffee)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.CoffeeResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	//functional variable for database connection
	// Create db connection
	db := utils.ConnectDB().Database("cafe")
	//get image associated with it
	var imageBytes []byte
	bucket, err := gridfs.NewBucket(db)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}
	imageStream, err := bucket.OpenDownloadStream(coffee.ImageFileID)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}
	defer imageStream.Close()

	imageBytes, err = io.ReadAll(imageStream)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{
			"error": true,
			"msg":   err.Error(),
		})
	}

	return c.Status(http.StatusOK).JSON(responses.CoffeeResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{
		"data":      coffee,
		"imageData": imageBytes,
	}})
}
