from m1_project_agne import krepsinis
from io import StringIO
from typing import Any, Callable, Literal
import pandas as pd



CRAWLERS: dict[str, Callable[..., pd.DataFrame]] = {
    "krepsinis": krepsinis.crawl_krepsinis,
}

def crawl(
    source: Literal["krepsinis"],
    return_format: Literal["csv", "df", "records"] = "csv",
    **kwargs,
) -> pd.DataFrame or str or list[dict[str, Any]]:

    if source not in CRAWLERS:
        raise ValueError(f"Source '{source}' is not supported.")

    data = CRAWLERS[source](**kwargs)

    if return_format == "df":
        return data
    elif return_format == "csv":
        with StringIO() as out:
            data.to_csv(out)
            content = out.getvalue()
        return content
    elif return_format == "records":
        return data.to_dict(orient="records")

if __name__ == "__main__":
    print(crawl("krepsinis", return_format="csv_file",base_url="https://www.krepsinis.net", time_limit=2))