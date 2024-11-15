from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pandas as pd

class IDataSource(ABC):
    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        pass

class IDataManager(ABC):
    @abstractmethod
    def refresh_data(self) -> Dict[str, pd.DataFrame]:
        pass
    
    @abstractmethod
    def load_cached_data(self, filename: str) -> pd.DataFrame:
        pass

class IChartService(ABC):
    @abstractmethod
    def create_chart(self, data: pd.DataFrame, chart_type: str) -> Optional[Any]:
        pass 