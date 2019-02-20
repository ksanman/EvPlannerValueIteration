def ToJson(instance):
    return {k:v for k , v in vars(instance).items() if not str(k).startswith('_')}

from address_info import AddressInfo
from charger import Charger
from user import User
from connection import Connection
from user_comment import UserComment
from media_item import MediaItem
import json

class ChargerContext:
    def __init__(self):
        pass

    def GetChargersFromJson(self, jsonData):
        """
        Gets the charger objects from the US charger request json file saved locally. 
        """
        chargers = []
        for data in jsonData:
            chargers.append(self.ObjectDecoder(data))
        return chargers

    def GetChargersFromFile(self, filePath):
        """
        Load the nearest chargers from a file. 
        """
        with open(filePath, 'r') as f:
            data = json.loads(f.read())

        return self.GetChargersFromJson(data)

    def AddressDecoder(self, addressInfo):
        """
        Function used to decode a json string into an AddressInfo object. 
        """
        return AddressInfo(addressInfo['AccessComments'] if 'AccessComments' in addressInfo else None,
            addressInfo['AddressLine1'] if 'AddressLine1' in addressInfo else None,
            addressInfo['AddressLine2'] if 'AddressLine2' in addressInfo else None,
            addressInfo['ContactEmail'] if 'ContactEmail' in addressInfo else None,
            addressInfo['ContactTelephone1'] if 'ContactTelephone1' in addressInfo else None,
            addressInfo['ContactTelephone2'] if 'ContactTelephone2' in addressInfo else None,
            addressInfo['CountryID'] if 'CountryID' in addressInfo else None,
            addressInfo['DistanceUnit'] if 'DistanceUnit' in addressInfo else None,
            addressInfo['ID'] if 'ID' in addressInfo else None,
            addressInfo['Latitude'] if 'Latitude' in addressInfo else None,
            addressInfo['Longitude'] if 'Longitude' in addressInfo else None,
            addressInfo['Postcode'] if 'Postcode' in addressInfo else None,
            addressInfo['RelatedUrl'] if 'RelatedUrl' in addressInfo else None,
            addressInfo['StateOrProvince'] if 'StateOrProvince' in addressInfo else None,
            addressInfo['Title'] if 'Title' in addressInfo else None,
            addressInfo['Town'] if 'Town' in addressInfo else None)

    def ObjectDecoder(self, obj):
        """
        Function used to decode a json string into a Charger object. 
        """
        if 'AddressInfo' in obj:
            addressInfo = obj['AddressInfo']
            a_info= self.AddressDecoder(addressInfo)

        if "Connections" in obj:
            connections = []
            for c in obj['Connections']:
                connections.append(Connection(
                    c["Amps"] if 'Amps' in c else None,
                    c["ConnectionTypeID"] if 'ConnectionTypeID' in c else None,
                    c["CurrentTypeID"] if 'CurrentTypeID' in c else None,
                    c["ID"] if 'ID' in c else None,
                    c["LevelID"] if 'LevelID' in c else None,
                    c["PowerKW"] if 'PowerKW' in c else None,
                    c["Quantity"] if 'Quantity' in c else None,
                    c["StatusTypeID"] if 'StatusTypeID' in c else None,
                    c["Voltage"] if 'Voltage' in c else None,
                ))

        mediaItems = []
        if "MediaItems" in obj:
            for m in obj["MediaItems"]:
                try:
                    mediaItems.append(MediaItem(
                        User(m["User"]["ID"],
                                m["User"]["ProfileImageURL"] if 'ProfileImageURL' in m['User'] else None,
                                m["User"]["ReputationPoints"] if 'ReputationPoints' in m['User'] else None,
                                m["User"]["Username"] if 'Username' in m['User'] else None
                        ) if 'User' in m else None,
                        m["ChargePointID"] if 'ChargePointID' in m else None,
                        m["Comment"] if 'Comments' in m else None,
                        m["DateCreated"] if 'DateCreated' in m else None,
                        m["ID"] if 'ID' in m else None,
                        m["IsEnabled"] if 'IsEnabled' in m else None,
                        m["IsExternalResource"] if 'IsExternalResource' in m else None,
                        m["IsFeaturedItem"] if 'IsFeaturedItem' in m else None,
                        m["IsVideo"] if 'IsVideo' in m else None,
                        m["ItemThumbnailURL"] if 'ItemThumbnailURL' in m else None,
                        m["ItemURL"] if 'ItemURL' in m else None
                    ))
                except Exception as e:
                    print('Media Item Exception: ', e)
                    print(m)
        userComments = []         
        if "UserComments" in obj:
            for u in obj["UserComments"]:
                try:
                    userComments.append(UserComment(
                        User(u["User"]["ID"],
                                u["User"]["ProfileImageURL"] if 'ProfileImageURL' in u['User'] else None,
                                u["User"]["ReputationPoints"] if 'ReputationPoints' in u['User'] else None,
                                u["User"]["Username"] if 'Username' in u['User'] else None
                        ) if 'User' in u else None,
                        u["ChargePointID"] if 'ChargePointID' in u else None,
                        u["CheckinStatusTypeID"] if 'CheckinStatusTypeID' in u else None,
                        u["CommentTypeID"] if 'CommentTypeID' in u else None,
                        u["DateCreated"] if 'DateCreated' in u else None,
                        u["ID"] if 'ID' in u else None,
                        u["Rating"] if 'Rating' in u else None,
                        u["UserName"] if 'UserName' in u else None
                    ))
                except Exception as e:
                    print('User Comment Exception: ', e)
                    print(u)

        charger = Charger(a_info, connections, mediaItems, userComments,
            obj["DataProviderID"] if 'DataProviderID' in obj else None,
            obj["DataQualityLevel"] if 'DataQualityLevel' in obj else None,
            obj["DateCreated"] if 'DateCreated' in obj else None,
            obj["DateLastStatusUpdate"] if 'DateLastStatusUpdate' in obj else None,
            obj["DateLastVerified"] if 'DateLastVerified' in obj else None,
            obj["GeneralComments"] if 'GeneralComments' in obj else None,
            obj["ID"] if 'ID' in obj else None,
            obj["IsRecentlyVerified"] if 'IsRecentlyVerified' in obj else None,
            obj["NumberOfPoints"] if 'NumberOfPoints' in obj else None,
            obj["OperatorID"] if 'OperatorID' in obj else None,
            obj["StatusTypeID"] if 'StatusTypeID' in obj else None,
            obj["SubmissionStatusTypeID"] if 'SubmissionStatusTypeID' in obj else None,
            obj["UUID"] if 'UUID' in obj else None,
            obj["UsageCost"] if 'UsageCost' in obj else None,
            obj["UsageTypeID"] if 'UsageTypeID' in obj else None
            )

        return charger