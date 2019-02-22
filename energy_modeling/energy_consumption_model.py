import math



class EnergyConsumptionModel:
    """ Model used to simulate ev battery consumption. 

        Based on this paper: https://www.researchgate.net/publication/294112610_Power-based_electric_vehicle_energy_consumption_model_Model_development_and_validation
    """
    GravitationAcceleration = 9.8066 #[m/s^2]
    AirDensity = 1.2256 #[kg/m^3]
    
    def ComputePowerToWheels(self, vehicle, acceleration, velocity, roadGrade, roadConditions):
        """ Equation:
            Pwheels(t) = (ma(a) + mg * cos(theta) * (c_r/1000)(c_1v(t) + c_2) + (1/2) * rho_air * A_f * C_d * v^2(t) + mg*sin(theta)) * v(t)

            Where:
            Pwheels = the power to the vehicles wheels
            m = vehicle mass (m =1521^2kg for Nissan Leaf)
            a(t) = dv(t)/dt (acceleration of vehicle in [m/s]^2) and can be negative
            g = 9.8066 [m/s^2]
            theta = road grade
            c_r = 1.75 - Rolling resistance parameter
            c_1 = 0.0328 - Rolling resistance parameter
            c_2 = 4.575 - Rolling resistance parameter
            p_air = 1.2256 [kg/m^3] air density
            A_f = frontal area of vehicle (2.3316 m^2 for leaf)
            c_d =  drag coefficient of vehicle (0.28 for leaf)
            v(t) speed of vehicle in [m/s]
        """
        powerToWheels = ((vehicle.Mass * acceleration) + (vehicle.Mass * self.GravitationAcceleration) * math.cos(roadGrade) \
            * (roadConditions.CR / 1000) * (roadConditions.C1 * velocity + roadConditions.C2) + 0.5 * self.AirDensity * vehicle.FrontalArea * vehicle.DragCoefficient * math.pow(velocity, 2) \
                + (vehicle.Mass * self.GravitationAcceleration) * math.sin(roadGrade)) * velocity

        return powerToWheels

    def ComputeTractionPowerAtMotor(self, powerAtWheels, vehicle):
        """ Equation:
            Pelectricmotor(t) = Pwheels * 1+ (1 -nu_drivetrain) * 1+ (1 - nu_electricmotor)
        """
        
        powerAtMotor = powerAtWheels * (1 + (1 - vehicle.DrivelineEfficiency)) * (1 + (1 - vehicle.MotorEfficiency))
        return powerAtMotor

    def ComputeRegenerationPowerAtMotor(self, powerAtMotor, vehicle):
        """ Equation:
            Pelectricmotor(t) = Pelectricmotor(t) * nu_rb(t)t
        """
        pass

    def ComputerFinalStateOfCharge(self):
        """
            SOC_final(t) = SOC_0 - sum_i=0^N deltaSOC_i(t)
        """
        pass

    def ComputeChangeInStateOfCharge(self):
        """
            deltaSOC_i(t) = SOC_i-1)(t) - (P_electricmotornet_i(t)/3600*Capacity_battery)

            P_electricmotornet_i(t) = Power consumed considering a battery efficiency of 90% and power consumed by auxilary systems (P_Auxiliary = 700 W)
            Capacity_battery is in Wh
            SOC_0 <= 95% >= 20%
        """
        pass

    def ComputeEnergyConsumption(self):
        """
            EC [kWh/km] = (1/3600000) * integral_0^t P_electricmotor_net(t)dt * (1/d)
        """
        pass

    def ComputeRegenerativeBraking(self):
        """
            nu_rb [%] = (E_recoverable [kWh]/ E_Available [kWh])
        """
        pass

    def ComputeEAvailable(self):
        """
            E_available [kWh] = integrate_0^t P_wheels_negative(t) dt
        """
        pass

    def ComputeNrb(self):
        """
            u_rb = a(t) < 0 then e^(0.0411/abs(a(t)))^-1
                    a(t) >=0 then 0
        """
        pass

    def ComputeERecoverable(self):
        """
            E_recoverable = n_rb * E_available
        """
        pass