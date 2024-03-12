import servo
def main():
    POWERS = [86.38E-6, 148.8E-6]
    DISTANCES = [2200, 3800]

    #DISTANCES, POWERS, _ = servo.ask_for_defined_points()
    data = servo.get_data("servo-attempt-1.csv")
    well_defined_data = servo.get_rows_with_known_displacement(data, POWERS)
    speed = servo.characterise_speed(well_defined_data, DISTANCES)
    servo.convert_time_to_displacement(data, well_defined_data, speed)

if __name__ == "__main__":
    main()
