import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
public class InsertTab {

	public static void main(String[] args) throws ClassNotFoundException {
		// TODO Auto-generated method stub
		Connection conn = null;
		javaTomysql test = new javaTomysql();
		try { 
			//連接MySQL
            Class.forName("com.mysql.jdbc.Driver");
            System.out.println("連接成功MySQLToJava");
            //建立讀取資料庫 (test 為資料庫名稱; user 為MySQL使用者名稱; passwrod 為MySQL使用者密碼)
            String datasource = "jdbc:mysql://localhost/ivrt_tab?user=irhw&password=irhw1234";
            
            conn = DriverManager.getConnection(datasource);
            System.out.println("連接成功MySQL"); 
            
            Statement st = conn.createStatement(); 
            st.executeUpdate("INSERT INTO ivrt " + 
                "VALUES (1001, 'Simpson', 'Mr.', 'Springfield', 2001)"); 
            

            conn.close(); 
        } catch (Exception e) { 
            System.err.println("Got an exception! "); 
            System.err.println(e.getMessage()); 
        }
		
	}

}
