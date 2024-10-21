// definir la base de datos y colecciones que se crearán
var dbName = 'db_mongo';
var collectionName = 'posts';
var collectionName2 = 'comentarios';
var collectionName3 = 'reacciones';

// crea una conexión a la base de datos 'admin' para realizar operaciones de administración
var adminDb = db.getSiblingDB('admin');

// autentica con un usuario administrador que tenga permisos para crear bases de datos y colecciones
adminDb.auth('root', 'password');

// crea la base de datos db_surveys
adminDb.createCollection(dbName);

// usa la base de datos recién creada
var dbMongo = db.getSiblingDB(dbName);

// crea la colección surveys dentro de la base de datos db_surveys
dbMongo.createCollection(collectionName);
dbMongo.createCollection(collectionName2);
dbMongo.createCollection(collectionName3);


dbMongo[collectionName].insertMany([
  {   
      "usuario_id": 1,
      "text": 'Pruebita 1',
      "images": [],
      "reacciones": [],
      "comentarios": []
  },
  {
    "usuario_id": 1,
    "text": 'Pruebita 2',
    "images": [],
    "reacciones": [],
    "comentarios": []
  }])
