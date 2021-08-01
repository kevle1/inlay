# TODO: Convert into proper test cases 
from util.inspect import process_site, process_url
import yaml

with open("conf.yaml", "r") as c: cfg = yaml.safe_load(c) 
sites = cfg["sites"]

def test(url):
    site, url = process_site(url, sites) 
    print(f"SITE {site} URL {url}")
    embed = process_url(url, site)
    print(embed)

def test_direct(url):
    print(f"URL {url}")
    embed = process_url(url, None, direct=True)
    print(embed)

if __name__ == "__main__":
    test("https://twitter.com/svblxyz/status/1411409142993113093")

    # NOTE: Reddit will return        https://v.redd.it/otk1nwrsb0971/DASH_720.mp4 
    #       the audio file will be at https://v.redd.it/otk1nwrsb0971/DASH_audio.mp4

    test("https://www.reddit.com/r/CitiesSkylines/comments/ocz17t/a_lot_of_hours_gone_into_this_wild_west/")
    test("https://www.reddit.com/r/NatureIsFuckingLit/comments/of1spb/iceberg_tsunamis_are_scarier_than_normal_tsunamis/?context=3")
    
    test("https://www.reddit.com/r/Damnthatsinteresting/comments/oj7qcb/lightning_bolt_is_guided_to_ground_through_rocket/")

    test_direct("https://www.youtube.com/watch?v=P656ZUf7gkU")
    test_direct("https://youtu.be/CZ3wIuvmHeM")
    test_direct("https://preview.redd.it/yvazj1h8dxb71.gif?width=851&format=mp4&s=f927bc782f2c7dc79ce53a0dcae4000e06de1f2b")
    test("https://www.reddit.com/r/AbruptChaos/comments/oujpqt/leap_of_faith/")