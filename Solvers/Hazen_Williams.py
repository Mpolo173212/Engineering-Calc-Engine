# solvers/Hazen_Williams.py

def calculate_headloss(Q, C, D, L):
    """
    Calculate headloss using the Hazen-Williams equation.

    Parameters:
        Q (float): Flow rate in cfs
        C (float): Hazen-Williams coefficient
        D (float): Diameter in feet
        L (float): Pipe length in feet

    Returns:
        float: Headloss in feet
    """
    return 10.67 * L * (Q ** 1.852) / ((C ** 1.852) * (D ** 4.87))
