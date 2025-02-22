from api.taptools_api import get_portfolio_trended_value


def main():
   response = get_portfolio_trended_value("stake1uxhvr22njt6fvq8jwyv958vcc9r2pa8q8zwk9t5nxvlfe7sz82fr7", "30d", "ADA")
   print(response)
   
if __name__ == "__main__":
    main()