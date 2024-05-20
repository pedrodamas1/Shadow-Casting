import numpy as np
import matplotlib.pyplot as plt


def convert_sph2cart(r, theta, phi) -> np.ndarray:
	x = r * np.sin(phi) * np.cos(theta)
	y = r * np.sin(phi) * np.sin(theta)
	z = r * np.cos(phi)
	return np.array([x,y,z]).transpose()

def calc_vector_magnitude(vector: np.ndarray) -> float:
	return np.linalg.norm(vector, axis=1)

def calc_angle_between(vector1: np.ndarray, vector2: np.ndarray) -> float:
	# Dot product formula: a.b = |a||b|cos(theta)
	a_dot_b = np.dot(vector1, vector2)
	mag_a = calc_vector_magnitude(vector1)
	mag_b = calc_vector_magnitude(vector2)
	return np.arccos(a_dot_b, mag_a*mag_b)


class Sun:

	def __init__(self, azimuth: float, altitude: float) -> None:
		self.azimuth = azimuth
		self.altitude = altitude
	
	@property
	def zenith(self) -> float:
		return np.pi/2 - self.altitude
	
	@property
	def theta(self) -> float:
		return np.pi/2 - self.azimuth
	
	def position_vector(self) -> np.ndarray:
		return np.zeros_like(self.direction_vector())
	
	def direction_vector(self, radius: float = 1) -> np.ndarray:
		return convert_sph2cart(radius, self.theta, self.zenith)

	def shadow_length(self, height: float = 1) -> float:
		return np.abs(1/np.tan(self.altitude)) * height
	
	def shadow_direction(self) -> np.ndarray:
		x = self.shadow_length() * np.cos(self.theta + np.pi)
		y = self.shadow_length() * np.sin(self.theta + np.pi)
		z = np.zeros_like(self.azimuth)
		return np.array([x,y,z]).transpose()


class Fixed:

	def __init__(self, direction_vector: np.ndarray) -> None:
		self.direction_vector = direction_vector

	def position_vector(self) -> np.ndarray:
		return np.zeros_like(self.direction_vector)

	def incidente_angle(self, sun: Sun) -> float:
		return calc_angle_between(self.direction_vector, sun.direction_vector())


if __name__ == '__main__':
	# time azimuth altitude zenith theta
	# 11:30	172,61	73,97	16,03	-82,61

	azimuth = 172.61*np.pi/180
	altitude = 73.97*np.pi/180
	#azimuth = np.array([60.53, 86.68, 143.36, 164.51, 282.32]) * np.pi/180
	#altitude = np.array([1.88, 34.71, 71.01, 73.59, 22.81]) * np.pi/180
	sun = Sun(azimuth, altitude)

	inclination = 34 * np.pi/180
	direction_vector = np.array([0, -np.cos(np.pi/2 - inclination), np.sin(np.pi/2 - inclination)])
	#N = len(azimuth)
	#direction_vector = np.tile(direction_vector, (N,1))
	fixed = Fixed(direction_vector)
	#print(fixed.incidente_angle(sun))
	a = sun.direction_vector()
	b = fixed.direction_vector
	mag_a = calc_vector_magnitude(a)
	mag_b = calc_vector_magnitude(b)
	print()

	


	# ax = plt.figure().add_subplot(projection='3d')
	# xyz = sun.position_vector().transpose()
	# uvw = sun.direction_vector().transpose()
	# ax.quiver(*xyz, *uvw, colors='orange')
	# uvw = sun.shadow_direction().transpose()
	# ax.quiver(*xyz, *uvw)
	# ax.quiver(*xyz, 0, 0, 1, colors='green')

	# ax.set_xlim3d([-1, 1])
	# ax.set_ylim3d([-1, 1])
	# ax.set_zlim3d([0, 1])
	# ax.set_xlabel('x')
	# ax.set_ylabel('y')
	# ax.set_zlabel('z')
	# ax.set_aspect('equal')
	# plt.show()