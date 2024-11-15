from typing import Dict, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate_age(value: Any) -> bool:
        try:
            age = float(value)
            return 0 <= age <= 120
        except:
            return False

    @staticmethod
    def validate_days_in_captivity(value: Any) -> bool:
        try:
            days = float(value)
            return days >= 0
        except:
            return False

    @staticmethod
    def validate_name(value: Any) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def validate_location(value: Any) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0

    def validate_record(self, record: Dict[str, Any]) -> Dict[str, bool]:
        return {
            'age': self.validate_age(record.get('age', -1)),
            'name': self.validate_name(record.get('name', '')),
            'location_taken': self.validate_location(record.get('location_taken', '')),
            'days_in_captivity': self.validate_days_in_captivity(record.get('days_in_captivity', -1))
        }

    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate dataframe and add validation status column"""
        try:
            validation_results = df.apply(self.validate_record, axis=1)
            df['validation_status'] = validation_results.apply(
                lambda x: 'valid' if all(x.values()) else 'invalid'
            )
            return df
        except Exception as e:
            logger.error(f"Error validating dataframe: {str(e)}")
            return df 