import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://rootuser:rootpassword@mongo-0.mongo-headless.kiii.svc.cluster.local:27017,mongo-1.mongo-headless.kiii.svc.cluster.local:27017,mongo-2.mongo-headless.kiii.svc.cluster.local:27017/courses?replicaSet=rs0')