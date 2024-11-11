package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/siamliam12/coffee_store/routes"
	"github.com/siamliam12/coffee_store/utils"
)

func main() {
	app := fiber.New()
	app.Use(cors.New())
	app.Use(logger.New())

	//db setup
	utils.ConnectDB()

	//routes
	routes.CoffeeRoute(app)

	app.Listen(":8000")
}
