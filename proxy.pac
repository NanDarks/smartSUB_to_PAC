// Generated at 17997150357

function findProxyForURL(url_address, host_address) {
  var myProxy = "PROXY www.speedtest.net:443; SOCKS5 www.speedtest.net:443";

  var domains_to_direct = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "*.ir",
    "ir",
    "iran",
    "irib",
    "mihan",
    "telewebion",
    "*.mihanblog.com",
    "*.mihanb.com",
    "*.irna.ir",
    "*.farsnews.com"
  ];
  
  for (var i = 0; i < domains_to_direct.length; i++) {
    if (shExpMatch(host_address, domains_to_direct[i])) {
      return "DIRECT";
    }
  }

  return myProxy;
}
