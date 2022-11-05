# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/20 3:25
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/6/7 13:07
from golf_federated.utils.log import loggerhear
from flask_sqlalchemy import SQLAlchemy


def table_init(
        dbname: str,
        db: SQLAlchemy
) -> None:
    """

    Initialize the tables in the database.
    Currently this part is just an example.
    The content of the table and related operation functions will be added later.

    Args:
        dbname (str): Name of the database.
        db (flask_sqlalchemy.SQLAlchemy): Database.

    """

    loggerhear.log("Common Info  ", 'Tables in %s are initializing' % (dbname))

    # Database table for user-related information.
    class USER_INFO(db.Model):
        # Define name of table.
        __tablename__ = 'USER_INFO'

        # User registered username.
        username = db.Column(db.String(20), primary_key=True)

        # Login password corresponding to username.
        password = db.Column(db.String(20), nullable=False)

    loggerhear.log("Common Info  ", 'Creating table USER_INFO')

    # Database table for service-related information.
    class SERVICE_INFO(db.Model):
        # Define name of table.
        __tablename__ = 'SERVICE_INFO'

        # Name of the service.
        servicename = db.Column(db.String(20), primary_key=True)

        # Service profile.
        servicebrief = db.Column(db.String(50), nullable=False)

        # Service details.
        servicedetail = db.Column(db.String(50), nullable=False)

        # Whether the service has a trained model.
        iftrained = db.Column(db.Boolean, nullable=False)

        # Whether the service is trained.
        iftrainable = db.Column(db.Boolean, nullable=False)

        # ID of the administrator responsible for this service.
        adminid = db.Column(db.String(20), nullable=False)

        # ID of the service consumer.
        userid = db.Column(db.String(20), nullable=False)

    loggerhear.log("Common Info  ", 'Creating table SERVICE_INFO')

    # Database table for global-model-related information.
    class GLOBAL_MODEL_INFO(db.Model):
        # Define name of table.
        __tablename__ = 'GLOBAL_MODEL_INFO'

        # Name of the service.
        servicename = db.Column(db.String(20), primary_key=True, nullable=False)

        # Model version.
        modelversion = db.Column(db.Integer, primary_key=True, nullable=False)

        # Maximum number of aggregation rounds.
        maxround = db.Column(db.Integer, nullable=True)

        # Federated aggregate type.
        aggregationtiming = db.Column(db.String(20), nullable=True)

        # Target accuracy.
        epsilon = db.Column(db.Float, nullable=True)

        # Number of samples for a single input to the model.
        batchsize = db.Column(db.Integer, nullable=True)

        # Learning rate.
        lr = db.Column(db.Float, nullable=True)

        # Initialization time.
        initializetime = db.Column(db.DateTime, nullable=True)

        # Number of updates.
        updatenum = db.Column(db.Integer, nullable=True)

        # Last update time.
        updatetime = db.Column(db.DateTime, nullable=True)

        # Path to model parameter file.
        modelpath = db.Column(db.String(20), nullable=True)

    loggerhear.log("Common Info  ", 'Creating table GLOBAL_MODEL_INFO')
