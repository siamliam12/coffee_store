package controllers

import (
	"context"
	"net/http"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"github.com/siamliam12/coffee_store/models"
	"github.com/siamliam12/coffee_store/responses"
	"github.com/siamliam12/coffee_store/utils"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var coffeeCollection *mongo.Collection = utils.GetCollection(utils.DB, "coffee")
var validate = validator.New()

func CreateCoffee(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var coffee models.Coffee
	defer cancel()

	//validate the request body
	if err := c.BodyParser(&coffee); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}
	//USE the validator library to validate required fields
	if validationErr := validate.Struct(&coffee); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}
	newCoffee := models.Coffee{
		Id:          primitive.NewObjectID(),
		Name:        coffee.Name,
		Price:       coffee.Price,
		Description: coffee.Description,
		Sizes:       coffee.Sizes,
		Category:    coffee.Category,
		Flavour:     coffee.Flavour,
	}
	result, err := coffeeCollection.InsertOne(ctx, newCoffee)
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.CoffeeResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}
	return c.Status(http.StatusCreated).JSON(responses.CoffeeResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})

}
