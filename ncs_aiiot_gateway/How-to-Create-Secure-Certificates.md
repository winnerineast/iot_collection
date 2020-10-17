# How to create secure certificates

## Warning - here is to have self-signed certificates for your testing or play but not used in production.

## Possible fixes
You could manually add a new (self-signed) root certificate to all devices needing access to your internal services so that your self-signed certificates are trusted - try getting that past the rest of the family!

The only other alternative is to use a trusted CA. Since I’m assuming you are doing this for testing or for use at home, I also assume that you don’t want to spend lots of money. Trusted certificates usually cost - a lot! Often US$100 per year or more.

However, there is one supplier that issues free trusted certificates. [Let’s Encrypt](https://letsencrypt.org/). This is a great service for a great price. But it comes with some overheads.