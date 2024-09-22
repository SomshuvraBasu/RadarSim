import math

def calculateFSPL(distance, frequency):
    """Calculate free space path loss."""
    c = 3e8  # speed of light in m/s
    wavelength = c / frequency
    fspl = (4 * math.pi * distance / wavelength) ** 2
    return fspl

def calculateReceivedPower(pt, gain_transmit, gain_receive, carrier_wavelength, rcs, distance):
    """Calculate received power."""
    received_power = (pt * gain_transmit * gain_receive * (carrier_wavelength ** 2) * rcs) / ((4 * math.pi) ** 3 * distance ** 4)
    return received_power

def calculateNoisePower(noise_figure, k, t0, frequency, bandwidth=1):
    """Calculate noise power."""
    noise_power = k * (noise_figure * t0 + t0) * bandwidth
    return noise_power

def calculateDopplerShift(relative_velocity, frequency):
    """Calculate Doppler shift."""
    c = 3e8  # speed of light in m/s
    doppler_shift=frequency * (c + relative_velocity) / (c - relative_velocity) - frequency
    return doppler_shift 

def calculateSNR(signal_power, noise_power):
    """Calculate Signal-to-Noise Ratio in dB."""
    snr = 10 * math.log10(signal_power / noise_power)
    return snr

def calculateJammingEffect(signal_power, jamming_power):
    """Calculate the effect of jamming on the signal."""
    effective_power = signal_power / (1 + jamming_power)
    return  effective_power