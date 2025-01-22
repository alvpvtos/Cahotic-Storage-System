
# Chaotic-Storage-System
> Note: This project is not ready for production. There are many features such as an user interface that need to be built and bugs that need to be fixed. 
> If you have questions about it, do not hesitate to reach out to me via [email](mailto:cahoticss@alvpvtos.com).

You might be asking yourself, "What the hell is a chaotic storage system?"
Well, after thinking about it, I couldn't answer that question myself, so here is what the almighty ChatGPT had to say. 
>A chaotic storage system is an organizational approach used in warehouses and distribution centers where items are stored in randomly assigned locations rather than in fixed, categorized spots. Each item's position is tracked using a digital system, often relying on barcodes or RFID tags to record and retrieve its location. This method contrasts with conventional storage, where similar items are grouped together in predefined sections. Chaotic storage leverages technology to maintain efficiency, prioritizing optimization of available space and adaptability to inventory changes over physical orderliness.

>The main advantages of chaotic storage are its flexibility and space utilization. It allows for the dynamic allocation of storage locations, which reduces wasted space and enables quick adaptation to inventory fluctuations. Additionally, it minimizes the time required to find or allocate space for new items, as workers rely on the system to guide them rather than manually searching for a suitable location. Companies with large and diverse inventories, such as e-commerce giants like Amazon, benefit significantly from this system. It streamlines operations in environments with high turnover rates, varying product sizes, and unpredictable demand patterns, ultimately improving efficiency and reducing operational costs.

Visual learner? Take a look at the following [video](https://www.youtube.com/watch?v=5TL80_8ACPc) to see Amazon's chaotic storage system in action. 

## Setup
### Prerequisites

The only tools needed to run this program are [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).  (I strongly recommend installing Docker Desktop if possible.)

Before proceeding, make sure you can successfully run the following commands in your terminal:
```sh
docker run hello-world
```
```sh
docker compose version
```

### Get the files 
Clone this repo and `cd` into it.
```sh
git clone https://github.com/alvpvtos/Cahotic-Storage-System.git && cd Cahotic-Storage-System
```

### Run the program

```sh
docker compose up
```

If everything went well, you should be able to head over to http://localhost:8080/docs and see the documentation for this API. 

Tip: Install [Postman](https://www.postman.com/downloads/), copy the entire JSON response from http://localhost:8080/openapi.json, and [send it to Postman](https://learning.postman.com/docs/integrations/available-integrations/working-with-openAPI/) for better visualization of the docs.

