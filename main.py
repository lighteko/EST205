from crawler import Crawler

def main():
    print("""
          WELCOME TO CRAWLER V1.0
            Please select the mode you would like to use:
            0: Google Play Store
            1: Apple App Store
            2: Reddit
          """)
    mode = int(input("Enter the mode: "))
    c = Crawler(mode)
    c.run()

if __name__ == "__main__":
    main()