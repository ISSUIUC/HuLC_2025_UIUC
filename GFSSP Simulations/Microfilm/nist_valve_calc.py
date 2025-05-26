import math

# Thermal Conductivity Coefficients (W/(m·K))
a_tc = 2.7380
b_tc = -30.677
c_tc = 89.430
d_tc = -136.99
e_tc = 124.69
f_tc = -69.556
g_tc = 23.320
h_tc = -4.3135
i_tc = 0.33829

# Specific Heat Coefficients (J/(kg·K))
a_cp = 31.88256
b_cp = -166.51949
c_cp = 352.01879
d_cp = -393.44232
e_cp = 259.98072
f_cp = -104.61429
g_cp = 24.99276
h_cp = -3.20792
i_cp = 0.16503




def evaluate_log10_polynomial_cp(T, a, b, c, d, e, f, g, h, i):
    """
    Evaluates the function:
    log10(y) = a + b*log10(T) + c*log10(T)^2 + ... + i*log10(T)^8
    Returns y = 10^log10(y)

    Parameters:
        T: Temperature in K (must be > 0)
        a to i: Coefficients

    Returns:
        y: Evaluated property
    """
    if T <= 0:
        raise ValueError("Temperature must be greater than zero.")
    
    logT = math.log10(T)
    log_y = a
    coeffs = [b, c, d, e, f, g, h, i]
    
    for power, coeff in enumerate(coeffs, start=1):
        log_y += coeff * (logT ** power)
    
    cp_SI = 10 ** log_y  # J/(kg·K)
    cp_Imperial = cp_SI * 0.0002388459  # Convert to BTU/(lbm·°R)
    
    return cp_Imperial


def evaluate_log10_polynomial_K(T, a, b, c, d, e, f, g, h, i):
    """
    Evaluates the function:
    log10(y) = a + b*log10(T) + c*log10(T)^2 + ... + i*log10(T)^8
    Returns y = 10^log10(y)

    Parameters:
        T: Temperature in K (must be > 0)
        a to i: Coefficients

    Returns:
        y: Evaluated property
    """
    if T <= 0:
        raise ValueError("Temperature must be greater than zero.")
    
    logT = math.log10(T)
    log_y = a
    coeffs = [b, c, d, e, f, g, h, i]
    
    for power, coeff in enumerate(coeffs, start=1):
        log_y += coeff * (logT ** power)
    
    k_SI = 10 ** log_y  #W/(m-K)
    k_Imperial = k_SI * 0.0001605  # Convert to BTU(s-ft-R)
    
    return k_Imperial


def generate_cp_data_cp(temp_start_K, temp_end_K, num_points):
    step = (temp_end_K - temp_start_K) / (num_points - 1)
    data = []
    for i in range(num_points):
        T_K = temp_start_K + i * step
        T_R = T_K * 9 / 5  # Convert to Rankine for output
        cp = evaluate_log10_polynomial_cp(T_K, a_cp, b_cp, c_cp, d_cp, e_cp, f_cp, g_cp, h_cp, i_cp)
        data.append((T_R, cp))  # Use Rankine in the output
    return data

def generate_k_data_k(temp_start_K, temp_end_K, num_points):
    step = (temp_end_K - temp_start_K) / (num_points - 1)
    data = []
    for i in range(num_points):
        T_K = temp_start_K + i * step
        T_R = T_K * 9 / 5  # Convert to Rankine for output
        k = evaluate_log10_polynomial_K(T_K, a_tc, b_tc, c_tc, d_tc, e_tc, f_tc, g_tc, h_tc, i_tc)
        data.append((T_R, k))  # Use Rankine in the output
    return data



def write_data_to_file(filename, data):
    with open(filename, 'w') as f:
        for T, val in data:
            f.write(f"{T:.4f} {val:.9f}\n")

# Generate data from 4 K to 300 K (50 points)
cp_data = generate_cp_data_cp(4, 300, 50)

K_data = generate_k_data_k(4, 300, 50)

# Save to file
write_data_to_file("./LCD_CORRECT_MICROFILM/user1Cp.prp", cp_data)
write_data_to_file("./LCD_CORRECT_MICROFILM/user1K.prp", K_data)