
class Event:

    def __init__(self, community_name, title, date, venue, description, link):
        self.community_name = community_name
        self.title = title
        self.day = self.__get_day(date)
        self.hour = self.__get_hour(date)
        self.venue = venue
        self.description = description
        self.link = link

    @staticmethod
    def from_json(json_dict):
        return Event(
            json_dict['community_name'],
            json_dict['title'],
            json_dict['date'],
            json_dict['venue'],
            json_dict['description'],
            json_dict['link'],
        )

    def __get_day(self, date):
        return date.split('T')[0]

    def __get_hour(self, date):
        return date.split('T')[1]
