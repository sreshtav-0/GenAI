import math

def mpg_to_kmpl(mpg: float, *, precision: int = 2) -> float:
    # Constants
    MILE_TO_KM = 1.609344
    GALLON_TO_L = 3.785411784
    
    # Validate mpg
    if not isinstance(mpg, (int, float)) or not math.isfinite(mpg) or mpg < 0:
        raise ValueError("mpg must be a finite, non-negative number.")
    
    # Validate precision
    if not isinstance(precision, int) or not (0 <= precision <= 10):
        raise ValueError("precision must be an integer between 0 and 10.")
    
    # Conversion factor
    conversion_factor = MILE_TO_KM / GALLON_TO_L
    
    # Perform conversion
    kmpl = mpg * conversion_factor
    
    # Return rounded result
    return round(kmpl, precision)


conversion_num = input("Enter the miles per gallon (mpg) value to convert: ")
print(f"You entered: {conversion_num} miles per gallon MPG to convert into kilometers per liter KPH/L. The converted value is: {mpg_to_kmpl(float(conversion_num))} KPH/L.")
