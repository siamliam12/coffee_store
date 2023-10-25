package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Coffee struct {
	Id          primitive.ObjectID `json:"id,omitempty"`
	Name        string             `json:"name,omitempty" validate:"required"`
	Price       float64            `json:"price,omitempty" validate:"required"`
	Description string             `json:"description,omitempty" validate:"required"`
	Sizes       string             `json:"sizes,omitempty" validate:"required"`
	Category    string             `json:"category,omitempty" validate:"required"`
	Flavour     string             `json:"flavour,omitempty" validate:"required"`
}
