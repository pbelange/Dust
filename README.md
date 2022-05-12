# Dust
Module to compute charging currents on dust grains

## Notes:
1. Only `Copper` and `Alumine` have the required properties to compute the SEY (see `Backend/Materials`). For other materials, the properties will have to be added from the litterature. 
2. The `DustObject` class can be used to keep all properties of a given dust grain together, as well as to get the charge `DustObject.Q` associated with a given surface potential `DustObject.phi`, since the two properties are interdependant. 

## Example
`demo.py` shows how to compute the SEY of a material, as well as how to compute the different currents based on a vector of surface potential.
<p align="center">
  <img src=./figures/SEY_curve.png  width="500">
</p>

<p align="center">
  <img src=./figures/Charging_currents.png  width="500">
</p>
