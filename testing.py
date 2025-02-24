from api.taptools_api import get_portfolio_trended_value

def main():
   response = get_portfolio_trended_value("stake1uxxt4u6wtqlce967axugyg0ta2xufawthegj2e7rj2rnh9sgrwt6d","30d","ADA")

   print(response)
   
if __name__ == "__main__":
    main()
