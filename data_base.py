import sqlite3
import time
import folium
from typing import NoReturn
import matplotlib.pyplot as plt


class Database:
    '''
        Class that encapsulates the database operations.

        Attributes
        ----------
            __DB_LOCATION : str
                The file path where the database is stored.
            __db_connection : sqlite3.Connection
                Object that uses to interact with the SQLite database.

        Methods
        -------
            __init__() -> NoReturn:
                Creates a new database connection and initializes the tables.
            __del__() -> NoReturn:
                Closes the database connection when the object is destroyed.
            __create_tabales__() -> NoReturn:
                Initializes the tables if they do not exist.
            user_exist(id: int) -> bool:
                Returns True if the user with the given id exists in the database, False otherwise.
            add_user(user: dict) -> NoReturn:
                Inserts a new user into the database.
            add_register(data: dict, user_id: int, is_real_location: bool) -> NoReturn:
                Inserts a new register into the database.
            get_registers_from_epoch(epoch: int) -> list:
                Returns a list of registers since a specific epoch.
            count_users() -> int:
                Returns the number of users in the database.
            draw_locations_in_a_map_and_statistics(epoch: int=0, opath: str='stat/') -> NoReturn:
                Creates a map with registered locations and some statistics about the data.
    '''

    __DB_LOCATION = 'data_base.db'


    def __init__(self) -> NoReturn:
        '''
            Creates a new database connection and initializes the tables.
        '''
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__create_tabales__()


    def __del__(self) -> NoReturn:
        '''
            Closes the database connection when the object is destroyed.
        '''
        self.__db_connection.close()


    def __create_tabales__(self) -> NoReturn:
        '''
            Initializes the tables if they do not exist.
        '''

        self.__db_connection.execute('PRAGMA foreign_keys = 1')

        sql = '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,
                                                   is_bot VARCHAR(255) NOT NULL,
                                                   first_name VARCHAR(255),
                                                   last_name VARCHAR(255),
                                                   username VARCHAR(255) NOT NULL,
                                                   language_code VARCHAR(2) NOT NULL
                                                  );'''
        self.__db_connection.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS registers (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       user_id INTEGER,
                                                       localtime INTEGER,
                                                       lat FLOAT,
                                                       lon FLOAT,
                                                       country VARCHAR(255) NOT NULL,
                                                       region VARCHAR(255) NOT NULL,
                                                       temperature INTEGER NOT NULL,
                                                       weather_code temperature INTEGER NOT NULL,
                                                       weather_descriptions VARCHAR(255) NOT NULL,
                                                       wind_speed INTEGER NOT NULL,
                                                       wind_degree INTEGER NOT NULL,
                                                       wind_dir VARCHAR(3) NOT NULL,
                                                       pressure INTEGER NOT NULL,
                                                       precip INTEGER NOT NULL,
                                                       humidity INTEGER NOT NULL,
                                                       cloudcover INTEGER NOT NULL,
                                                       feelslike INTEGER NOT NULL,
                                                       uv_index INTEGER NOT NULL,
                                                       visibility INTEGER NOT NULL,
                                                       is_day BOOLEAN NOT NULL,
                                                       is_real_location BOOLEAN NOT NULL,
                                                       server_time INTEGER,
                                                       FOREIGN KEY(user_id) REFERENCES users(id)
                                                      );'''
        self.__db_connection.execute(sql)


    def user_exist(self, id: int) -> bool:
        '''
            Checks if a user with given id exists in the database.

            Parameters
            ----------
                id : int
                    The id of the user to be checked.
            Returns
            -------
                bool
                    True if user exists, False otherwise.
        '''
        cursor = self.__db_connection.cursor()
        query = 'SELECT COUNT(*) FROM users WHERE id=?'
        result = cursor.execute(query, (id,)).fetchone()
        return result[0] > 0


    def add_user(self, user: dict) -> NoReturn:
        '''
            Adds a new user to the database.

            Parameters
            ----------
                user: int
                    A dictionary containing user data.
        '''
        cursor = self.__db_connection.cursor()
        query = '''INSERT INTO users (id, is_bot, first_name, last_name, username, language_code)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, (user['id'], user['is_bot'], user['first_name'], user['last_name'],
                               user['username'], user['language_code']))
        self.__db_connection.commit()


    def add_register(self, data: dict, user_id: int, is_real_location: bool, server_time: int) -> NoReturn:

        '''
            Adds a new register to the database.

            Parameters
            ----------
            data : dict
                A dictionary containing register data.
            user_id : int
                The id of the user who made the register.
            is_real_location : bool
                True if the register is made with real location, False otherwise.
            server_time : int
                The time server is running.
        '''
        cursor = self.__db_connection.cursor()
        query = '''INSERT INTO registers (user_id, localtime, lat, lon, country, region,
                                          temperature, weather_code, weather_descriptions,
                                          wind_speed, wind_degree, wind_dir,
                                          pressure, precip, humidity, cloudcover,
                                          feelslike, uv_index, visibility, is_day,
                                          is_real_location, server_time)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, (user_id, data['localtime'], data['lat'],
                               data['lon'], data['country'], data['region'],
                               data['temperature'], data['weather_code'],
                               ', '.join(data['weather_descriptions']),
                               data['wind_speed'], data['wind_degree'], data['wind_dir'],
                               data['pressure'], data['precip'], data['humidity'],
                               data['cloudcover'], data['feelslike'], data['uv_index'],
                               data['visibility'], data['is_day'], is_real_location,
                               server_time))
        self.__db_connection.commit()


    def get_registers_from_epoch(self, epoch: int) -> list:
        '''
            Returns a list of registers since a specific epoch.

            Parameters
            ----------
            epoch : int
                The epoch time from which registers are to be retrieved.

            Returns
            -------
            list
                A list of dictionaries containing register data.
        '''
        cursor = self.__db_connection.cursor()
        query = 'SELECT * FROM registers INNER JOIN users ON registers.user_id=users.id WHERE server_time >= ?'
        result = cursor.execute(query, (epoch,)).fetchall()

        registers = []
        for row in result:
            register = {'id': row[0], 'user_id': row[1], 'localtime': row[2], 'lat': row[3],
                        'lon': row[4], 'country': row[5], 'region': row[6],
                        'temperature': row[7], 'weather_code': row[8],
                        'weather_descriptions': row[9].split(', '), 'wind_speed': row[10],
                        'wind_degree': row[11], 'wind_dir': row[12], 'pressure': row[13],
                        'precip': row[14], 'humidity': row[15], 'cloudcover': row[16],
                        'feelslike': row[17], 'uv_index': row[18], 'visibility': row[19],
                        'is_day': row[20], 'is_real_location': row[21], 'username': row[26],
                        'server_time': row[27]}
            registers.append(register)
        return registers


    def count_users(self) -> int:
        '''
            Returns the number of users in the database.

            Returns
            -------
            int
                Number of users in the data base.
        '''
        cursor = self.__db_connection.cursor()
        query = 'SELECT COUNT(*) FROM users;'
        result = cursor.execute(query).fetchall()
        return result[0][0]


    def draw_locations_in_a_map_and_statistics(self, epoch: int = 0, opath: str = 'stat/') -> NoReturn:
        """
            This method creates a map with registered locations and some statistics about the data.

            Parameters
            ----------
            epoch : int
                The epoch timestamp from which to retrieve registers. If not specified,
                it defaults to the current timestamp minus one day (86400 seconds).
            opath : str
                The path where to save the output files. If not specified, it defaults to 'stat/'.

        """
        if epoch == 0:
            epoch = int(time.time()) - 86400
        if epoch < 0:
            epoch = 1
        registers = self.get_registers_from_epoch(epoch)

        # Create a map with all the registered locations
        map = folium.Map(location=[0, 0], zoom_start=2)
        for register in registers:
            popup_text = f"{register['username']}, {register['weather_descriptions'][0]}, {register['temperature']}°C"
            if register['is_real_location']:
                icon = folium.Icon(color="green")
            else:
                icon = folium.Icon(color="red")
            folium.Marker(location=[register['lat'], register['lon']], popup=popup_text, icon=icon).add_to(map)
        map.save(opath + time.strftime('%Y-%m-%d', time.localtime(epoch)) + '_map.html')

        # Create some statistics about the data
        temperatures = [register['temperature'] for register in registers]
        humidity = [register['humidity'] for register in registers]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.hist(temperatures, bins=20)
        ax1.set_xlabel('Temperature (°C)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Temperature Histogram')
        ax2.scatter(humidity, temperatures, alpha=0.5)
        ax2.set_xlabel('Humidity (%)')
        ax2.set_ylabel('Temperature (°C)')
        ax2.set_title('Temperature vs Humidity')
        plt.savefig(opath + time.strftime('%Y-%m-%d', time.localtime(epoch)) + '_statistics.png')

        print(f'Number of users: {self.count_users()}')
        print(f'Number of registers since epoch {time.strftime("%Y-%m-%d", time.localtime(epoch))}: {len(registers)}')
