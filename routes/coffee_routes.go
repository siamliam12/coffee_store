package routes

import (
	"github.com/gofiber/fiber/v2"
	"github.com/siamliam12/coffee_store/controllers"
)

func CoffeeRoute(app *fiber.App) {
	//all routes related to coffee comes here
	app.Post("/coffee", controllers.CreateCoffee)
}
