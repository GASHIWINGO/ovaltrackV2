from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Define the database engine.
# For PostgreSQL:
engine = create_engine('postgresql://postgres:123@localhost:5432/nascar') # Replace with your PostgreSQL connection details!

# Base class for declarative models
Base = declarative_base()

# Define the Series table
class Series(Base):
    __tablename__ = 'Series'

    id = Column(String, primary_key=True, comment="Series ID")
    name = Column(String, comment="Series Name (e.g., NASCAR Cup Series)")
    alias = Column(String, comment="Series Alias (e.g., CUP)")

    seasons = relationship("Season", back_populates="series") # Relationship to Season table
    races = relationship("Race", back_populates="series") # Relationship to Race table
    driver_standings = relationship("DriverStanding", back_populates="series") # Relationship to DriverStanding table

    def __repr__(self):
        return f"<Series(id='{self.id}', name='{self.name}', alias='{self.alias}')>"

# Define the Season table
class Season(Base):
    __tablename__ = 'Seasons'

    id = Column(String, primary_key=True, comment="Season ID")
    year = Column(Integer, comment="Season Year")
    start_date = Column(Date, comment="Season Start Date")
    end_date = Column(Date, comment="Season End Date")
    status = Column(String, comment="Season Status (e.g., scheduled, closed)")
    series_id = Column(String, ForeignKey('Series.id'), comment="Foreign key to Series table") # Foreign key to Series

    series = relationship("Series", back_populates="seasons") # Relationship to Series table
    races = relationship("Race", back_populates="season") # Relationship to Race table
    driver_standings = relationship("DriverStanding", back_populates="season") # Relationship to DriverStanding table

    def __repr__(self):
        return f"<Season(id='{self.id}', year={self.year}, status='{self.status}')>"

# Define the Driver table
class Driver(Base):
    __tablename__ = 'Drivers'

    id = Column(String, primary_key=True, comment="Driver ID")
    first_name = Column(String, comment="Driver First Name")
    last_name = Column(String, comment="Driver Last Name")
    full_name = Column(String, comment="Driver Full Name")
    status = Column(String, comment="Driver Status (e.g., ACT, INA)")
    image_url = Column(String, nullable=True, comment="URL of driver's image") # Added image_url column

    driver_standings = relationship("DriverStanding", back_populates="driver") # Relationship to DriverStanding table
    races_entered = relationship("RaceEntry", back_populates="driver") # Relationship to RaceEntry table

    def __repr__(self):
        return f"<Driver(id='{self.id}', full_name='{self.full_name}', status='{self.status}')>"

# Define the Team table (Car Owner)
class Team(Base):
    __tablename__ = 'Teams'

    id = Column(String, primary_key=True, comment="Team ID")
    name = Column(String, comment="Team Name")
    series_id = Column(String, ForeignKey('Series.id'), comment="Foreign key to Series table") # Foreign key to Series

    def __repr__(self):
        return f"<Team(id='{self.id}', name='{self.name}')>"

# Define the Track table
class Track(Base):
    __tablename__ = 'Tracks'

    id = Column(String, primary_key=True, comment="Track ID")
    name = Column(String, comment="Track Name")
    market = Column(String, comment="Track Market (City)")
    address = Column(String, nullable=True, comment="Track Address") # Added address column
    city = Column(String, nullable=True, comment="Track City") # Added city column
    state = Column(String, nullable=True, comment="Track State") # Added state column
    zip = Column(String, nullable=True, comment="Track Zip Code") # Added zip column
    country = Column(String, nullable=True, comment="Track Country") # Added country column
    lat = Column(Float, nullable=True, comment="Track Latitude")
    lng = Column(Float, nullable=True, comment="Track Longitude")
    completed = Column(Integer, nullable=True, comment="Year Track Completed")
    distance = Column(Float, comment="Track Distance (Miles)")
    shape = Column(String, comment="Track Shape (e.g., Oval, Road Course)")
    banking = Column(String, nullable=True, comment="Track Banking Description")
    frontstretch = Column(String, nullable=True, comment="Frontstretch Length")
    backstretch = Column(String, nullable=True, comment="Backstretch Length")
    owner = Column(String, nullable=True, comment="Track Owner")
    surface = Column(String, nullable=True, comment="Track Surface Type")
    track_type = Column(String, nullable=True, comment="Track Type")
    track_image_url = Column(String, nullable=True, comment="URL of track's aerial image") # Added track_image_url column

    races = relationship("Race", back_populates="track") # Relationship to Race table

    def __repr__(self):
        return f"<Track(id='{self.id}', name='{self.name}', market='{self.market}')>"

# Define the Race table (Event/Schedule)
class Race(Base):
    __tablename__ = 'Races'

    id = Column(String, primary_key=True, comment="Race ID")
    series_id = Column(String, ForeignKey('Series.id'), comment="Foreign key to Series table") # Foreign key to Series
    season_id = Column(String, ForeignKey('Seasons.id'), comment="Foreign key to Seasons table") # Foreign key to Seasons table
    track_id = Column(String, ForeignKey('Tracks.id'), comment="Foreign key to Tracks table") # Foreign key to Tracks table
    name = Column(String, comment="Race Name")
    number = Column(Integer, comment="Race Number in Season")
    status = Column(String, comment="Race Status (e.g., scheduled, complete)")
    distance = Column(Integer, comment="Race Distance")
    laps = Column(Integer, comment="Number of Laps in Race")
    chase_race = Column(Boolean, comment="Is Chase Race (Playoff Race)?")
    heat_race = Column(Boolean, nullable=True, comment="Is Heat Race?") # Added heat_race column
    award_pole = Column(Boolean, nullable=True, comment="Is Pole Awarded?") # Added award_pole column
    stage_count = Column(Integer, nullable=True, comment="Number of Stages")
    stage_1_laps = Column(Integer, nullable=True, comment="Laps in Stage 1")
    stage_2_laps = Column(Integer, nullable=True, comment="Laps in Stage 2")
    stage_3_laps = Column(Integer, nullable=True, comment="Laps in Stage 3")
    parent_id = Column(String, nullable=True, comment="Parent Race ID for grouping events") # Added parent_id column
    scheduled = Column(Date, nullable=True, comment="Scheduled Date")
    start_time = Column(Date, nullable=True, comment="Race Start Time")
    qualifying_start_time = Column(Date, nullable=True, comment="Qualifying Start Time")
    qualifying_status = Column(String, nullable=True, comment="Qualifying Status")
    practice_start_time = Column(Date, nullable=True, comment="Practice Start Time") # Example for practice time, you might need separate tables for practices/qualifying
    practice_status = Column(String, nullable=True, comment="Practice Status") # Example for practice status
    broadcast_network = Column(String, nullable=True, comment="Broadcast Network")
    broadcast_radio = Column(String, nullable=True, comment="Broadcast Radio")
    prior_winner_id = Column(String, nullable=True, comment="ID of prior race winner (Driver)") # You might need a separate table for prior winners if you want to store more details

    series = relationship("Series", back_populates="races") # Relationship to Series table
    season = relationship("Season", back_populates="races") # Relationship to Season table
    track = relationship("Track", back_populates="races") # Relationship to Track table
    race_entries = relationship("RaceEntry", back_populates="race") # Relationship to RaceEntry table

    def __repr__(self):
        return f"<Race(id='{self.id}', name='{self.name}', status='{self.status}')>"

# Define association table for many-to-many relationship between Race and Driver for entries
class RaceEntry(Base):
    __tablename__ = 'RaceEntries'

    race_id = Column(String, ForeignKey('Races.id'), primary_key=True, comment="Foreign key to Race table")
    driver_id = Column(String, ForeignKey('Drivers.id'), primary_key=True, comment="Foreign key to Driver table")
    team_id = Column(String, ForeignKey('Teams.id'), nullable=True, comment="Foreign key to Team table (optional)") # You can add Team if needed
    car_number = Column(String, nullable=True, comment="Car Number") # Example: Car number for the entry

    race = relationship("Race", back_populates="race_entries") # Relationship to Race table
    driver = relationship("Driver", back_populates="races_entered") # Relationship to Driver table
    team = relationship("Team") # Relationship to Team table (optional)

    def __repr__(self):
        return f"<RaceEntry(race_id='{self.race_id}', driver_id='{self.driver_id}')>"


# Define the DriverStandings table
class DriverStanding(Base):
    __tablename__ = 'DriverStandings'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Driver Standing ID (auto-increment)") # Auto-incrementing ID
    series_id = Column(String, ForeignKey('Series.id'), comment="Foreign key to Series table") # Foreign key to Series
    season_id = Column(String, ForeignKey('Seasons.id'), comment="Foreign key to Seasons table") # Foreign key to Seasons table
    driver_id = Column(String, ForeignKey('Drivers.id'), comment="Foreign key to Driver table") # Foreign key to Driver
    rank = Column(Integer, comment="Driver Rank in Standings")
    points = Column(Integer, comment="Driver Points")
    starts = Column(Integer, nullable=True, comment="Number of Starts")
    wins = Column(Integer, nullable=True, comment="Number of Wins")
    poles = Column(Integer, nullable=True, comment="Number of Poles")
    stage_wins = Column(Integer, nullable=True, comment="Number of Stage Wins")
    chase_bonus = Column(Integer, nullable=True, comment="Chase Bonus Points")
    chase_wins = Column(Integer, nullable=True, comment="Number of Chase Wins")
    chase_stage_wins = Column(Integer, nullable=True, comment="Number of Chase Stage Wins")
    top_5 = Column(Integer, nullable=True, comment="Number of Top 5 Finishes")
    top_10 = Column(Integer, nullable=True, comment="Number of Top 10 Finishes")
    top_15 = Column(Integer, nullable=True, comment="Number of Top 15 Finishes")
    top_20 = Column(Integer, nullable=True, comment="Number of Top 20 Finishes")
    dnf = Column(Integer, nullable=True, comment="Number of Did Not Finish (DNF)")
    laps_led = Column(Integer, nullable=True, comment="Number of Laps Led")
    laps_completed = Column(Integer, nullable=True, comment="Number of Laps Completed")
    money = Column(Float, nullable=True, comment="Money Earned (Prize Money)")
    avg_start_position = Column(Float, nullable=True, comment="Average Start Position")
    avg_finish_position = Column(Float, nullable=True, comment="Average Finish Position")
    avg_laps_completed = Column(Float, nullable=True, comment="Average Laps Completed")
    laps_led_pct = Column(Float, nullable=True, comment="Percentage of Laps Led")
    gained_lost = Column(Integer, nullable=True, comment="Rank change from previous week") # Added gained_lost column
    in_chase = Column(Boolean, nullable=True, comment="Is Driver in the Chase (Playoffs)?")

    series = relationship("Series", back_populates="driver_standings") # Relationship to Series table
    season = relationship("Season", back_populates="driver_standings") # Relationship to Season table
    driver = relationship("Driver", back_populates="driver_standings") # Relationship to Driver table

    def __repr__(self):
        return f"<DriverStanding(driver_id='{self.driver_id}', rank={self.rank}, points={self.points})>"


# Create all tables in the database
Base.metadata.create_all(engine)

print("Database schema created successfully!")