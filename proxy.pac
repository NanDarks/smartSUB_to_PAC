// Generated at 17985998973

function findProxyForURL(url_address, host_address) {
  var myProxy = "PROXY 172.66.44.235:443; SOCKS5 172.66.44.235:443";

  var domains_to_proxy = [
    "*.youtube.com",
    "*.googlevideo.com",
    "*.twitter.com",
    "*.instagram.com",
    "*.telegram.org",
    "*.wikipedia.org",
    "*.facebook.com",
    "*.linkedin.com",
    "*.tiktok.com"
  ];
  
  for (var i = 0; i < domains_to_proxy.length; i++) {
    if (shExpMatch(host_address, domains_to_proxy[i])) {
      return myProxy;
    }
  }

  return "DIRECT";
}
