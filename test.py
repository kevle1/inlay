import unittest

import yaml
from util.embed import generate_embed, parse_site


class TestURLProcessing(unittest.TestCase):
    def setUp(self):
        with open("conf.yaml", "r") as c:
            self.cfg = yaml.safe_load(c)
        self.sites = self.cfg["sites"]

    def test_process_url_twitter(self):
        url = "https://twitter.com/svblxyz/status/1411409142993113093"
        site, url = parse_site(url, self.sites)
        self.assertEqual(site, "twitter")
        embed = generate_embed(url, site)
        self.assertIsNotNone(embed)

    def test_process_url_reddit(self):
        url = "https://www.reddit.com/r/CitiesSkylines/comments/ocz17t/a_lot_of_hours_gone_into_this_wild_west/"
        site, url = parse_site(url, self.sites)
        self.assertEqual(site, "reddit")
        embed = generate_embed(url, site)
        self.assertIsNotNone(embed)

    def test_process_url_reddit_with_context(self):
        url = "https://www.reddit.com/r/NatureIsFuckingLit/comments/of1spb/iceberg_tsunamis_are_scarier_than_normal_tsunamis/?context=3"
        site, url = parse_site(url, self.sites)
        self.assertEqual(site, "reddit")
        embed = generate_embed(url, site)
        self.assertIsNotNone(embed)

    def test_process_url_direct_youtube(self):
        url = "https://www.youtube.com/watch?v=P656ZUf7gkU"
        embed = generate_embed(url, None, direct=True)
        self.assertIsNotNone(embed)

    def test_process_url_direct_youtu_be(self):
        url = "https://youtu.be/CZ3wIuvmHeM"
        embed = generate_embed(url, None, direct=True)
        self.assertIsNotNone(embed)

    def test_process_url_direct_reddit_preview(self):
        url = "https://preview.redd.it/yvazj1h8dxb71.gif?width=851&format=mp4&s=f927bc782f2c7dc79ce53a0dcae4000e06de1f2b"
        embed = generate_embed(url, None, direct=True)
        self.assertIsNotNone(embed)

    def test_process_url_reddit_leap_of_faith(self):
        url = "https://www.reddit.com/r/AbruptChaos/comments/oujpqt/leap_of_faith/"
        site, url = parse_site(url, self.sites)
        self.assertEqual(site, "reddit")
        embed = generate_embed(url, site)
        self.assertIsNotNone(embed)


if __name__ == "__main__":
    unittest.main()
