// definir la base de datos y colecciones que se crearán
var dbName = 'db_mongo';
var collectionName = 'posts';
var collectionName2 = 'comentarios';
var collectionName3 = 'reacciones';
var collectionName4 = 'destinies';        // lugares destino que pueden estar asociados a un viaje
var collectionName5 = 'wishlists';       // lista de viajes deseados por el usuario
var collectionName5 = 'travels';          // viajes realizados por el usuario usuario con destinos asociados

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
dbMongo.createCollection(collectionName4);
dbMongo.createCollection(collectionName5);


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
