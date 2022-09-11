import java.io.File;

import py4j.GatewayServer;
import unbbayes.prs.*;
import unbbayes.io.*;

public class Gateway {
  
  public static void main(String[] args) throws Exception  {
    Gateway app = new Gateway();
    
    
    // app is now the gateway.entry_point
    GatewayServer server = new GatewayServer(app);
    server.start();
  }
}


