"""
Engineering calculations for the Fluid Flow & Heat Transfer Suite.
"""

import math


class Fluid:
    """Stores the physical properties of a fluid."""

    def __init__(self, name, density, viscosity):
        """Create a fluid with density in kg/m3 and viscosity in Pa.s."""
        if density <= 0 or viscosity <= 0:
            raise ValueError("Density and viscosity must be greater than zero.")

        self.name = name
        self.density = density
        self.viscosity = viscosity


class Pipe:
    """Performs pipe-flow calculations."""

    def __init__(self, diameter, length, roughness):
        """Create a pipe using dimensions in metres."""
        if diameter <= 0:
            raise ValueError("Diameter must be greater than zero.")

        if length <= 0:
            raise ValueError("Length must be greater than zero.")

        if roughness < 0:
            raise ValueError("Roughness cannot be negative.")

        self.diameter = diameter
        self.length = length
        self.roughness = roughness

    def velocity(self, flow_rate):
        """Calculate average fluid velocity in m/s."""
        if flow_rate <= 0:
            raise ValueError("Flow rate must be greater than zero.")

        area = math.pi * self.diameter ** 2 / 4

        return flow_rate / area

    def reynolds_number(self, flow_rate, fluid):
        """Calculate Reynolds number."""
        velocity = self.velocity(flow_rate)

        return (
            fluid.density
            * velocity
            * self.diameter
            / fluid.viscosity
        )

    def friction_factor(self, flow_rate, fluid):
        """Calculate Darcy friction factor."""
        reynolds = self.reynolds_number(flow_rate, fluid)

        if reynolds < 2300:
            return 64 / reynolds

        relative_roughness = self.roughness / self.diameter

        return (
            -1.8
            * math.log10(
                (relative_roughness / 3.7) ** 1.11
                + 6.9 / reynolds
            )
        ) ** -2

    def pressure_drop(self, flow_rate, fluid):
        """Calculate pressure drop using Darcy-Weisbach."""
        velocity = self.velocity(flow_rate)

        friction = self.friction_factor(
            flow_rate,
            fluid,
        )

        return (
            friction
            * (self.length / self.diameter)
            * (fluid.density * velocity ** 2 / 2)
        )


class HeatTransfer:
    """Performs basic heat-transfer calculations."""

    @staticmethod
    def conduction_heat_rate(
        thermal_conductivity,
        area,
        hot_temperature,
        cold_temperature,
        thickness,
    ):
        """Calculate heat transfer through a flat wall."""
        if thermal_conductivity <= 0:
            raise ValueError("Thermal conductivity must be positive.")

        if area <= 0 or thickness <= 0:
            raise ValueError("Area and thickness must be positive.")

        return (
            thermal_conductivity
            * area
            * (hot_temperature - cold_temperature)
            / thickness
        )

    @staticmethod
    def cooling_time(
        density,
        specific_heat,
        volume,
        heat_transfer_coefficient,
        area,
        initial_temperature,
        target_temperature,
        ambient_temperature,
    ):
        """Calculate cooling time using Newton's law of cooling."""

        if density <= 0 or specific_heat <= 0:
            raise ValueError("Material properties must be positive.")

        if volume <= 0 or heat_transfer_coefficient <= 0:
            raise ValueError("Volume and heat-transfer coefficient must be positive.")

        if area <= 0:
            raise ValueError("Area must be positive.")

        ratio = (
            (target_temperature - ambient_temperature)
            / (initial_temperature - ambient_temperature)
        )

        if ratio <= 0 or ratio >= 1:
            raise ValueError(
                "Target temperature must be between the initial and ambient temperatures."
            )

        return -(
            density
            * specific_heat
            * volume
            / (heat_transfer_coefficient * area)
        ) * math.log(ratio)

    @staticmethod
    def cooling_temperature(
        time,
        density,
        specific_heat,
        volume,
        heat_transfer_coefficient,
        area,
        initial_temperature,
        ambient_temperature,
    ):
        """Calculate temperature at a given time."""

        tau = (
            density
            * specific_heat
            * volume
            / (heat_transfer_coefficient * area)
        )

        return ambient_temperature + (
            initial_temperature - ambient_temperature
        ) * math.exp(-time / tau)