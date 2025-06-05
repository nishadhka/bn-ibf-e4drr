## ECMWF SEAS5 Dataset

The European Centre for Medium-Range Weather Forecasts (ECMWF) Seasonal Forecast System 5 (SEAS5) is a comprehensive seasonal forecasting dataset that provides ensemble predictions for meteorological variables up to 13 months ahead.

**Temporal Coverage:**
- Forecast lead times: 1-13 months
- Hindcast period: 1981-2016 (for model validation)
- Real-time forecasts: 2017 onwards
- Initialization frequency: Monthly (around the 1st of each month)

**Spatial Resolution:**
- Atmospheric model: ~36 km horizontal resolution (TCo319 spectral resolution)
- Ocean model: ~25 km resolution (ORCA025)
- Land surface model: Same as atmospheric grid

**Ensemble Configuration:**
- 51 ensemble members for real-time forecasts
- 25 ensemble members for hindcasts
- Ensemble generation through perturbed initial conditions and stochastic physics

**Key Variables Include:**
- **Surface variables**: 2-meter temperature, precipitation, mean sea level pressure, surface winds, soil moisture, snow depth
- **Upper-air variables**: Temperature, geopotential height, winds at multiple pressure levels
- **Ocean variables**: Sea surface temperature, ocean heat content, mixed layer depth
- **Derived indices**: El Niño Southern Oscillation indices, Arctic Oscillation, North Atlantic Oscillation

**Data Characteristics:**
- Monthly mean values are the primary output
- Daily data available for some variables
- Probabilistic information provided through ensemble spread
- Bias-corrected products available for some applications

## CHIRPS Dataset

The Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) is a high-resolution precipitation dataset designed primarily for drought monitoring and climate trend analysis.

**Temporal Coverage:**
- Period: 1981 to near real-time (updated with ~3 weeks delay)
- Temporal resolution: Daily, pentadal (5-day), dekadal (10-day), and monthly
- Consistent 40+ year record for climate analysis

**Spatial Coverage:**
- Geographic extent: 50°S to 50°N (focusing on tropics and subtropics)
- Horizontal resolution: 0.05° × 0.05° (~5.3 km at equator)
- Covers all land areas within the latitude band

**Data Sources and Methodology:**
- **Satellite infrared data**: Primary input from geostationary satellites
- **Microwave precipitation estimates**: From polar-orbiting satellites
- **Station observations**: Ground-based precipitation measurements for bias correction
- **Climatology**: CHPclim (Climate Hazards Group Precipitation climatology)

**Key Features:**
- **Primary variable**: Precipitation (mm/day or mm/period)
- **Quasi-global coverage**: Emphasis on data-sparse regions in developing countries
- **Bias correction**: Incorporates station data to reduce satellite-only biases
- **Consistent methodology**: Uniform processing across the entire time series

**Data Products:**
- **CHIRPS v2.0**: Standard resolution (0.05°)
- **CHIRPSv2.0**: Includes additional station data
- **Preliminary products**: Near real-time versions with shorter latency
- **Anomaly products**: Standardized precipitation index and percentile rankings

**Applications:**
- Drought monitoring and early warning systems
- Agricultural yield forecasting
- Water resource management
- Climate change impact studies
- Food security assessments

Both datasets serve complementary purposes: SEAS5 provides seasonal forecasting capabilities for multiple meteorological variables with ensemble uncertainty quantification, while CHIRPS offers high-resolution, long-term precipitation observations optimized for climate monitoring and trend analysis in vulnerable regions.