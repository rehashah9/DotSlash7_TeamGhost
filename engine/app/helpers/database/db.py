from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import create_engine, MetaData, Table, select, Connection



class CloudDatabase:
    def __init__(self) -> None:
        self.engine = create_engine(f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/postgres")
        self.metadata = self.initialize_metadata()

    def initialize(self) -> create_engine:
        engine = create_engine(f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/postgres")
        return engine

    def initialize_metadata(self) -> MetaData:
        metadata = MetaData()
        metadata.reflect(self.engine)
        return metadata


main_db = CloudDatabase()