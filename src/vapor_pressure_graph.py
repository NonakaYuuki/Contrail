import numpy as np
import matplotlib.pyplot as plt

class Vapor_pressure:
    def __init__(self,
                 Tmin,
                 Tmax):
        self.Tmin = int(Tmin + 273.15)
        self.Tmax = int(Tmax + 273.15)
        self.T_list = [t for t in range(self.Tmin, self.Tmax+1, 1)]
        self.T_list_c = [t for t in range(Tmin, Tmax+1, 1)]

    def Ew(self):
        result = []
        for T in self.T_list:
            result.append(np.exp(
            54.842763
            - 6763.22 / (T)
            - 4.210 * np.log(T)
            + 0.000367 * (T)
            + np.tanh(0.0415 * (T - 218.8))
            * (
                53.878
                - 1331.22 / (T)
                - 9.44523 * np.log(T)
                + 0.014025 * (T)
            )
        ) / 100)
        return result
    
    def Ei(self):
        result = []
        for T in self.T_list:
            result.append(np.exp(
            9.550426
            - 5723.265 / (T)
            + 3.53068 * np.log(T)
            - 0.00728332 * (T)
        ) / 100)
        return result
    
    def Ei_Ew(self):
        result = []
        for T in self.T_list:
            result.append(- np.exp(
            9.550426
            - 5723.265 / (T)
            + 3.53068 * np.log(T)
            - 0.00728332 * (T)
        ) + np.exp(
            54.842763
            - 6763.22 / (T)
            - 4.210 * np.log(T)
            + 0.000367 * (T)
            + np.tanh(0.0415 * (T - 218.8))
            * (
                53.878
                - 1331.22 / (T)
                - 9.44523 * np.log(T)
                + 0.014025 * (T)
            )
        ))
        return result
    
    def Goff_Gratch(self):
        Tst = 372.15
        result = []
        for T in self.T_list:
            p = 10**(-7.90298 * (Tst/T - 1) + 5.02808 * np.log10(Tst/T) - 1.3816 * 10**(-7) * (10**(11.34 * (1 - T/Tst)) - 1) + 8.1328 * 10**(-3) * (10**(-3.49149 * (Tst/T - 1)) - 1) + np.log10(1013.246))
            result.append(p)
        return result
    
    def WMO(self):
        result = []
        for T in self.T_list:
            p = 10**(10.79574 * (1 - 273.16/T) - 5.02800 * np.log10(T/273.16) + 1.50475 * 10**-4 * (1 - 10**(-8.2969*(T/273.16-1))) + 0.42873 * 10**-3 * (10**(4.76955*(1-273.16/T)) - 1) + 0.78614)
            result.append(p)
        return result

    def Sonntag(self):
        result = []
        for T in self.T_list:
            p = np.e**(-6096.9385 / T + 16.635794 - 2.711193 * 10**-2 * T + 1.673952 * 10**-5 * T**2+ 2.433502 * np.log(T))
            result.append(p)
        return result
    
    def Goff_Gratch_ice(self):
        result = []
        T0 = 273.15
        for T in self.T_list:
            p = 10**(-9.09718 * (T0/T - 1) - 3.56654 * np.log10(T0/T) + 0.876793 * (1 - T/T0)) - 2.2195983 + np.log10(1013.246)
            result.append(p)
        return result
    
    def WMO_ice(self):
        result = []
        for T in self.T_list_c:
            p = 6.112 * np.e**(22.46 * T/(272.62 + T)) 
            result.append(p)
        return result
    
    def Malti_ice(self):
        result = []
        for T in self.T_list:
            p = -2663.5 / T + 12.537
            result.append(p)
        return result
    
    def AEKDi_ice(self):
        result = []
        for T in self.T_list_c:
            p = 6.1128 * np.e**(22.571 * T/(273.71 + T)) 
            result.append(p)
        return result
    
    def AEKR_water(self):
        result = []
        for T in self.T_list_c:
            p = 6.1094 * np.e**(17.625 * T/(273.71 + T)) 
            result.append(p)
        return result
    
    def vis(self):
        fig, ax = plt.subplots()
        ax.plot(self.T_list_c, self.Ew(), label='Ew', linewidth=3)
        ax.plot(self.T_list_c, self.Ei(), label='Ei', linewidth=3)
        # ax.plot(self.T_list_c, self.Goff_Gratch(), label='Goff Gratch Water', linewidth=3)
        # ax.plot(self.T_list_c, self.WMO(), label='WMO')
        # ax.plot(self.T_list_c, self.Sonntag(), label='Sonntag')
        # ax.plot(self.T_list_c, self.Goff_Gratch_ice(), label='Goff Gratch Ice', linewidth=3)
        # ax.plot(self.T_list_c, self.WMO_ice(), label='WMO_Ice')
        # ax.plot(self.T_list_c, self.Malti_ice(), label='Malti_Ice')
        ax.plot(self.T_list_c, self.AEKR_water(), label='AEKR_Water', linewidth=3)
        ax.plot(self.T_list_c, self.AEKDi_ice(), label='AEKDi_Ice', linewidth=3)
        
        plt.tick_params(labelsize=20)
        ax.set_xlabel('Temperature (°C)', fontsize=20, fontweight='bold')
        ax.set_ylabel('Vapor Pressure (hPa)', fontsize=20, fontweight='bold')
        ax.legend(fontsize=20)
        ax.grid(which = "both", axis = "y", color = "black", alpha = 0.8, linestyle = "--", linewidth = 1)
        plt.show()
        # plt.savefig('./result/vapor_pressure/test.png')

if __name__ == '__main__':
    # Tst = 372.15
    # T = 300
    # print(10**(-7.90298 * (Tst/T - 1) + 5.02808 * np.log10(Tst/T) - 1.3816 * 10**(-7) * (10**(11.34 * (1 - T/Tst)) - 1) + 8.1328 * 10**(-3) * (10**(-3.49149 * (Tst/T - 1)) - 1) + np.log10(1013.246)))
    vapor_pressure = Vapor_pressure(-50,10)
    vapor_pressure.vis()