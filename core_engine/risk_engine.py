import numpy as np

class SentinelRiskEngine:
    def __init__(self):
        # Weights perfectly matching your PRD formulation
        self.w_concentration = 0.20
        self.w_volatility = 0.15
        self.w_leverage = 0.25
        self.w_margin = 0.15
        self.w_behavioral = 0.15
        self.w_execution = 0.10

    def calculate_risk_score(self, order_params, portfolio, behavioral, market_depth):
        """
        Computes the case study Risk Score (RS) matrix bounded strictly between 0-100.
        """
        # 1. Concentration Index (C_idx)
        nominal_order_value = order_params['quantity'] * order_params['price']
        c_idx = min((nominal_order_value / portfolio['total_nav']) * 100, 100)

        # 2. Volatility Index (V_idx)
        v_idx = market_depth['iv_percentile']

        # 3. Leverage Index (L_idx)
        current_leverage = (portfolio['nominal_exposure'] + nominal_order_value) / portfolio['total_nav']
        l_idx = min((current_leverage / 10.0) * 100, 100)  # Standardized against 10x max cap

        # 4. Margin Utilization Index (M_idx)
        projected_margin = portfolio['margin_used'] + (nominal_order_value * 0.20)
        m_idx = min((projected_margin / portfolio['total_nav']) * 100, 100)

        # 5. Behavioral Anomaly Index (B_idx)
        b_idx = behavioral['revenge_coefficient'] * 100

        # 6. Execution Risk Index (E_idx)
        e_idx = market_depth['bid_ask_spread_pct'] * 50  # Scales spread variations elegantly

        # Composite Score Calculation Matrix
        raw_score = (
            (self.w_concentration * c_idx) +
            (self.w_volatility * v_idx) +
            (self.w_leverage * l_idx) +
            (self.w_margin * m_idx) +
            (self.w_behavioral * b_idx) +
            (self.w_execution * e_idx)
        )
        
        final_score = int(np.clip(raw_score, 0, 100))
        
        # State Allocation Engine
        if final_score >= 75:
            classification = "HIGH"
            action = "INTERCEPT_WITH_EXPLICIT_FRICTION"
        elif final_score >= 40:
            classification = "MODERATE"
            action = "INLINE_WARNING_ALERT"
        else:
            classification = "LOW"
            action = "PASSED_UNCHECKED"

        return {
            "risk_score": final_score,
            "risk_classification": classification,
            "action_required": action,
            "breakdown": {
                "Portfolio Concentration Index": int(c_idx),
                "Implied Volatility Index": int(v_idx),
                "Leverage Exposure Index": int(l_idx),
                "Margin Utilization Index": int(m_idx),
                "Behavioral Anomaly Index": int(b_idx),
                "Microstructure Execution Index": int(e_idx)
            }
        }