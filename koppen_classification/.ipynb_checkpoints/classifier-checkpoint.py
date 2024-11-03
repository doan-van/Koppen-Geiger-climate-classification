import numpy as np
import matplotlib.pyplot as plt

class KoppenClassification:
    def __init__(self, precip, temp, south):
        # Check if precip and temp arrays have 12 monthly values
        if len(precip) != 12 or len(temp) != 12:
            raise ValueError("Precipitation and temperature arrays must each contain 12 monthly values.")
        
        # Initialize input variables
        self.precip = precip           # Monthly precipitation values
        self.temp = temp               # Monthly temperature values
        self.south = bool(south)       # Boolean for hemisphere; True if southern hemisphere
        
        # Calculate basic climate statistics
        self.temp_mean = temp.mean()   # Mean annual temperature
        self.prcp_sum = precip.sum()   # Total annual precipitation
        self.prcp_min = precip.min()   # Minimum monthly precipitation
        self.temp_min = temp.min()     # Minimum monthly temperature
        self.temp_max = temp.max()     # Maximum monthly temperature
        self.nu_mon_gt10deg = (temp > 10).astype(int).sum()  # Number of months with temperature > 10°C
        
        # Define summer and winter months based on hemisphere
        # If in southern hemisphere, summer is from Oct-March; else Apr-Sept
        self.mon_sw = [[3, 4, 5, 6, 7, 8], [0, 1, 2, 9, 10, 11]]
        self.mon_ind = {'summer': self.mon_sw[1], 'winter': self.mon_sw[0]} if self.south else {'summer': self.mon_sw[0], 'winter': self.mon_sw[1]}
        
        # Separate seasonal precipitation data
        self.prcp_summer = precip[self.mon_ind['summer']]  # Precipitation in summer months
        self.prcp_winter = precip[self.mon_ind['winter']]  # Precipitation in winter months
        
        # Calculate precipitation threshold for climate classification
        self.prcp_threshold = self.calculate_precip_threshold()
        
        # Seasonal precipitation statistics
        self.prcp_summer_min = self.prcp_summer.min()  # Minimum summer precipitation
        self.prcp_summer_max = self.prcp_summer.max()  # Maximum summer precipitation
        self.prcp_winter_min = self.prcp_winter.min()  # Minimum winter precipitation
        self.prcp_winter_max = self.prcp_winter.max()  # Maximum winter precipitation
        
        # Perform classification
        self.koppen_class = self.classify()

    def calculate_precip_threshold(self):
        """
        Calculate the precipitation threshold based on seasonal precipitation distribution.
        This threshold determines aridity for climate classification:
        - Adjusted by annual temperature and distribution of rainfall.
        """
        if self.prcp_winter.sum() > 0.7 * self.prcp_sum:
            # Winter is wetter: basic threshold
            return 20 * self.temp_mean
        elif self.prcp_summer.sum() > 0.7 * self.prcp_sum:
            # Summer is wetter: threshold includes an additional adjustment
            return 20 * self.temp_mean + 280
        else:
            # Both seasons contribute rainfall: intermediate threshold adjustment
            return 20 * self.temp_mean + 140

    def classify(self):
        """
        Classifies the climate type according to the Köppen classification system.
        
        Classification is based on:
        - Total annual precipitation compared to the calculated threshold
        - Seasonal distribution of precipitation (summer vs. winter)
        - Temperature characteristics (mean, max, and min monthly temperatures)

        Returns:
            koppen_class (str): A Köppen climate classification code based on temperature and precipitation criteria.
        """
        
        # Group B: Arid climates - total precipitation is less than the threshold
        if self.prcp_sum < self.prcp_threshold:
            koppen_class = "B"  # Base classification for Arid climates
            
            # Determine specific arid subclass: Desert (BW) or Steppe (BS)
            koppen_class += "W" if self.prcp_sum < self.prcp_threshold / 2 else "S"
            
            # Temperature indicator for arid climates:
            # 'h' for hot, low-latitude (mean temp >= 18°C)
            # 'k' for cold, mid-latitude (mean temp < 18°C)
            koppen_class += "h" if self.temp_mean >= 18 else "k"
        
        # Group A: Tropical climates - all months have a temperature >= 18°C
        elif self.temp_min >= 18:
            koppen_class = "A"  # Base classification for Tropical climates
            
            # Further classification of Tropical climates based on monthly rainfall:
            if self.prcp_min >= 60:
                koppen_class += "f"  # Rainforest: all months have significant rainfall
            else:
                # Monsoon (Am) or Savanna (Aw) subtypes based on rainfall in the driest month
                koppen_class += "m" if self.prcp_min >= 100 - self.prcp_sum / 25 else "w"
        
        # Group C: Temperate climates - warmest month > 10°C and coldest month between 0°C and 18°C
        elif self.temp_max > 10 and 0 < self.temp_min < 18:
            koppen_class = "C"  # Base classification for Temperate climates
            
            # Determine dry season:
            # 's' for dry summer, 'w' for dry winter, 'f' for no distinct dry season
            if self.prcp_summer_min < 40 and self.prcp_summer_min < self.prcp_winter_max / 3:
                koppen_class += "s"  # Dry summer
            elif self.prcp_winter_min < self.prcp_summer_max / 10:
                koppen_class += "w"  # Dry winter
            else:
                koppen_class += "f"  # No dry season
            
            # Further classify based on summer temperatures:
            # 'a' for hot summer (max temp >= 22°C), 'b' for warm summer, 'c' for cool summer
            if self.temp_max >= 22:
                koppen_class += "a"
            elif self.nu_mon_gt10deg >= 4:
                koppen_class += "b"
            else:
                koppen_class += "c"
        
        # Group D: Continental climates - warmest month > 10°C and coldest month <= 0°C
        elif self.temp_max > 10 and self.temp_min <= 0:
            koppen_class = "D"  # Base classification for Continental climates
            
            # Determine dry season:
            # 's' for dry summer, 'w' for dry winter, 'f' for no distinct dry season
            if self.prcp_summer_min < 40 and self.prcp_summer_min < self.prcp_winter_max / 3:
                koppen_class += "s"  # Dry summer
            elif self.prcp_winter_min < self.prcp_summer_max / 10:
                koppen_class += "w"  # Dry winter
            else:
                koppen_class += "f"  # No dry season
            
            # Further classify based on temperature:
            # 'a' for hot summer (max temp >= 22°C), 'b' for warm summer, 'c' for cool summer,
            # 'd' for extremely cold winters (min temp < -38°C)
            if self.temp_max >= 22:
                koppen_class += "a"
            elif self.nu_mon_gt10deg >= 4:
                koppen_class += "b"
            elif self.temp_min < -38:
                koppen_class += "d"
            else:
                koppen_class += "c"
        
        # Group E: Polar climates - no month has a temperature > 10°C
        elif self.temp_max <= 10:
            koppen_class = "E"  # Base classification for Polar climates
            
            # Further subclassification:
            # 'T' for Tundra (temp > 0°C in at least one month)
            # 'F' for Ice Cap (no month above 0°C)
            koppen_class += "T" if self.temp_max > 0 else "F"
        
        # If none of the criteria match, classification is unknown
        else:
            koppen_class = 'Unknown'
        
        return koppen_class

    def summary(self):
        """
        Returns a summary dictionary containing climate statistics.
        Useful for output and reporting climate characteristics.
        """
        return {
            'mean temperature': self.temp_mean,
            'max temperature': self.temp_max,
            'min temperature': self.temp_min,
            'num of months hotter than 10 deg': self.nu_mon_gt10deg,
            'precip threshold': self.prcp_threshold,
            'minimum summer precip': self.prcp_summer_min,
            'maximum summer precip': self.prcp_summer_max,
            'minimum winter rain': self.prcp_winter_min,
            'maximum winter rain': self.prcp_winter_max,
            'annual accum rain': self.prcp_sum,
            'minimum monthly rain': self.prcp_min
        }

    def get_classification(self, writeout=False):
        """
        Returns the climate classification code, with an optional summary of statistics.
        :param writeout: If True, returns classification and climate summary dictionary
        """
        if writeout:
            return self.koppen_class, self.summary()
        else:
            return self.koppen_class

    def plot_hythergraph(self, title='Climograph'):
        """
        Plots a hythergraph showing monthly temperature and precipitation.
        
        Parameters:
        title (str): Title of the plot.
        
        Returns:
        matplotlib.figure.Figure: A figure object representing the plot.
        """
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        lab1, lab3 = 'Temperature (°C)', 'Precipitation (mm)'
        xlab, ylab1, ylab2 = 'Month', 'Temperature (°C)', 'Precipitation (mm)'

        # Create figure and axis
        fig = plt.figure(figsize=[8, 5])
        ax1 = plt.axes([.15, .2, .7, .65])

        # Plot temperature data
        ax1.plot(months, self.temp, 'o--', color='darkred', label=lab1)
        ax1.set_xlabel(xlab)
        ax1.set_ylabel(ylab1, color='darkred')
        ax1.tick_params(axis='y', labelcolor='darkred')

        # Create a second y-axis to plot precipitation
        ax2 = ax1.twinx()
        ax2.bar(months, self.precip, alpha=0.3, color='green', label=lab3)
        ax2.set_ylabel(ylab2, color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # Add title and show plot
        plt.title(title)
        fig.legend(loc='lower left', fontsize=9, ncols=2, bbox_to_anchor=(0.2, -0.05))

        return fig
