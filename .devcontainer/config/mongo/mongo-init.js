#!/usr/bin/env node
// This script is run when the container is started. It is used to initialize the database.
// The script is run as the root user, so it can create users and databases.
db = db.getSiblingDB('admin');

// move to the admin user
db.auth('root', 'developer');

// Initialize the Hyfi database and create two users with read/write access
db = db.getSiblingDB('Hyfi');

// Create the first user with username "alpha" and password "developer"
db.createUser({
  user: 'alpha',
  pwd: 'developer',
  roles: [
    {
      role: 'readWrite',
      db: 'Hyfi'
    }
  ]
});

// Create the second user with username "beta" and password "developer"
db.createUser({
  user: 'beta',
  pwd: 'developer',
  roles: [
    {
      role: 'readWrite',
      db: 'Hyfi'
    }
  ]
});

// Create the users collection
db.createCollection("users", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["name", "email", "password", "age"],
         properties: {
             _id: {
                bsonType: "objectId",
                description: "must be an objectId and is required",
                uniqueItems: true,
                default: new ObjectId()
             },
            name: {
               bsonType: "string",
               description: "required and must be a string"
            },
            email: {
               bsonType: "string",
               description: "required and must be a string representing an email address",
               pattern: "^\\S+@\\S+\\.\\S+$",
               uniqueItems: true
            },
            password: {
               bsonType: "string",
               description: "required and must be a string"
            },
            age: {
               bsonType: "int",
               description: "required and must be an integer"
            },
            roles: {
               bsonType: "array",
               description: "must be an array of strings",
               items: {
                  bsonType: "string"
               },
               default: ["user"]
            },
            last_updated: {
               bsonType: "date",
               description: "must be a date string in the format YYYY-MM-DD HH:MM:SS",
               default: new Date()
            }
         }
      }
   }
})


// // Insert the five users
// db.users.insertMany([
//     {
//         name: "John Doe",
//         password: "john123",
//         email: "john@example.com",
//         age: 25,
//         roles: ["admin", "user"]
//     },
//     {
//         name: "Jane Doe",
//         password: "jane123",
//         email: "jane@example.com",
//         age: 27
//     },
//     {
//         name: "Alice Jones",
//         password: "alice123",
//         email: "alice@example.com",
//         age: 23
//     },
//     {
//         name: "Bob Smith",
//         password: "bob123",
//         email: "bob@example.com",
//         age: 24
//     },
//     {
//         name: "James Cook",
//         password: "james123",
//         email: "james@example.com",
//         age: 29
//     }
// ]);
