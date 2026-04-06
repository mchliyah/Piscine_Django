import sys
import antigravity


def print_usage():
	print("Usage: python geohashing.py <latitude> <longitude> <date-dow>")
	print("Example: python geohashing.py 37 -122 2005-05-26-10458.68")


def main():
	if len(sys.argv) != 4:
		print("Error: invalid number of arguments.")
		print_usage()
		return 1

	try:
		latitude = int(sys.argv[1])
		longitude = int(sys.argv[2])
	except ValueError:
		print("Error: latitude and longitude must be integers.")
		print_usage()
		return 1

	datedow = sys.argv[3].encode("utf-8")

	try:
		antigravity.geohash(latitude, longitude, datedow)
	except Exception as exc:
		print(f"Error: {exc}")
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())