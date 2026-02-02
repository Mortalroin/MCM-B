class LogisticsConfig:
    TOTAL_MASS = 1.0e8
    PROGRESS_RATIO = 0.85
    EXPONENT_B = -np.log2(PROGRESS_RATIO)
    Q_MIN = 1.0e6
    SE_CAPACITY_ANNUAL = 537000
    RISK_ROCKET_FAILURE = 0.03
    RISK_SE_EFFICIENCY = (0.95, 0.02)
def get_rocket_unit_cost(year, cumulative_mass):
    q_eff = LogisticsConfig.Q_MIN + cumulative_mass
    ratio = q_eff / LogisticsConfig.Q_MIN
    decay = np.power(ratio, -LogisticsConfig.EXPONENT_B)
    return LogisticsConfig.COST_PMIN + (LogisticsConfig.COST_P0 - LogisticsConfig.COST_PMIN) * decay
def run_simulation(rocket_ratio):
    m_rocket_target = LogisticsConfig.TOTAL_MASS * rocket_ratio
    m_elevator_target = LogisticsConfig.TOTAL_MASS * (1 - rocket_ratio)
    mass_se, time_se = 0, 0
    while mass_se < m_elevator_target:
        eff = np.random.normal(*LogisticsConfig.RISK_SE_EFFICIENCY)
        actual_cap = LogisticsConfig.SE_CAPACITY_ANNUAL * np.clip(eff, 0.5, 1.0)
        mass_se += min(actual_cap, m_elevator_target - mass_se)
        time_se += 1
    mass_rk, time_rk, total_cost = 0, 0, 0
    while mass_rk < m_rocket_target:
        attempts = predict_launches(current_year)
        successes = np.random.binomial(attempts, 1 - LogisticsConfig.RISK_ROCKET_FAILURE)
        mass_this_year = successes * LogisticsConfig.ROCKET_PAYLOAD
        mass_rk += min(mass_this_year, m_rocket_target - mass_rk)
        unit_cost = get_rocket_unit_cost(current_year, mass_rk)
        total_cost += attempts * LogisticsConfig.ROCKET_PAYLOAD * unit_cost
        time_rk += 1
    return max(time_se, time_rk), total_cost