import carla
import math

HOST = 'isi-simcar.campusfc.dir.unibo.it'

class Sun:
    def __init__(self, azimuth, altitude):
        self.azimuth = azimuth  # Horizontal angle (degrees)
        self.altitude = altitude  # Vertical angle (degrees)
        self._t = 0.0  # Time factor to simulate movement

    def tick(self, delta_seconds):
        self._t += 0.01 * delta_seconds  # Control the speed of the sun's movement
        self.azimuth = (self._t * 180) % 360  # Simulate rotation from 0 to 180 degrees
        self.altitude = 100 * math.sin(math.radians(self.azimuth))  # Max altitude 100 degrees
    
    def __str__(self):
        return f'Sun(alt: {self.altitude:.2f}, azm: {self.azimuth:.2f})'


class Weather:
    def __init__(self, weather):
        self.weather = weather
        self._sun = Sun(0, 0)

    def tick(self, delta_seconds):
        self._sun.tick(delta_seconds)
        self.weather.sun_azimuth_angle = self._sun.azimuth
        self.weather.sun_altitude_angle = self._sun.altitude
    
    def get_weather(self):
        return self.weather

    def __str__(self):
        return str(self._sun)


def main():
    speed_factor = 5
    update_freq = 0.1 / speed_factor

    client = carla.Client(HOST, 2000)
    client.set_timeout(15.0)
    client.reload_world()
    world = client.get_world()

    spectator = world.get_spectator()
    transform = spectator.get_transform()
    transform.rotation.yaw += 240
    spectator.set_transform(transform)

    weather = Weather(world.get_weather())
    elapsed_time = 0.0

    while True:
        timestamp = world.wait_for_tick().timestamp
        elapsed_time += timestamp.delta_seconds
        if elapsed_time > update_freq:
            weather.tick(speed_factor * elapsed_time)
            world.set_weather(weather.get_weather())
            print(f'{weather}', end='\r')
            elapsed_time = 0.0


if __name__ == '__main__':
    main()
