from sonar import SonarSensor, StepperMotor, STEPDEFAULT

def test_distance_sensor():
    print("Starting sonar sensor test")
    dist = SonarSensor()
    print("SonarSensor constructed")
    dist.check()
    dist.close()

def test_stepper_motor():
    print("Starting stepper motor test")
    try:
        stepper = StepperMotor()
        stepper.set_zero()
        stepper.run_steps(2 * STEPDEFAULT, delay=0.005, truncate = False)
        stepper.run_zero()

    except KeyboardInterrupt:
        print("interrupted")
    finally:
        # stepper.set_zero()
        print(f"final stepcount: {stepper.motor_step}")
