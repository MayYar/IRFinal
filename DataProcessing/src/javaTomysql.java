import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
public class javaTomysql
{
    public static void main(String[] args) throws ClassNotFoundException 
    {
//    	ArrayList<Integer> id = new ArrayList<Integer>();
//    	ArrayList<String> term = new ArrayList<String>();
//    	ArrayList<String> loc = new ArrayList<String>();
        Connection conn = null;
        try
        {
            //連接MySQL
            Class.forName("com.mysql.jdbc.Driver");
            System.out.println("連接成功MySQLToJava");
            //建立讀取資料庫 (test 為資料庫名稱; user 為MySQL使用者名稱; passwrod 為MySQL使用者密碼)
            //String datasource = "jdbc:mysql://localhost/irdb?user=irhw&password=irhw1234";
            
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/irdb?useUnicode=yes&characterEncoding=UTF-8","irhw", "irhw1234");
            System.out.println("連接成功MySQL");
            Statement st = conn.createStatement();
            st.execute("SELECT * FROM all_words");	//從all_words挑出來到各doc比對
            
            //st.executeUpdate("TRUNCATE ivrt");
        	ResultSet rs = st.getResultSet();
        	DatabaseMetaData dbmd = conn.getMetaData();
        	Statement tabst = conn.createStatement();	//各資料庫裡找有沒這個字詞
        	while(rs.next()){
        		
        		System.out.print(rs.getString("word"));
        		//Thread.sleep(3);
        		StringBuilder ans = new StringBuilder();
        		
           		
        		ResultSet tabrs = dbmd.getTables(null,null,null,null);
        		while(tabrs.next()){
        			Thread.sleep(3);
	            	if(tabrs.getString(3).equals("all_words")||tabrs.getString(3).equals("ivrt"))	//跳過all_word table
	            		continue;
        			
            	//System.out.println(tabrs.getString(3));	//column 3 is table name
            	//撈出資料
		            	
		            	tabst.execute("SELECT * FROM " + tabrs.getString(3));
		            	ResultSet rs1 = tabst.getResultSet();
		            	while(rs1.next()){
		            		
		            		if(rs.getInt("word_ID") == (rs1.getInt("word_ID"))){
		            			System.out.print("," + tabrs.getString(3));
		            			ans.append(tabrs.getString(3) + ",");
		            			break;
		            		}//if
		            		//Thread.sleep(1);
		            	}//while	
	            	
        		}//while
        		//loc.add(ans);
        		System.out.println();

//                	String sql="INSERT INTO ivrt (id,word,location) VALUES (?,?,?)";//prepare statement
//                	 
//                    PreparedStatement pstmt = conn.prepareStatement(sql);
//                    pstmt.setString(1, rs.getString("word_ID"));//第一個?要插入的值
//                    pstmt.setString(2, rs.getString("word"));//第二個?要插入的值
//                    pstmt.setString(3, ans.toString());//第三個?要插入的值
//                    pstmt.executeUpdate();
                    
        			ans.setLength(1);
        			ans=null;
        			System.gc();
            }//while
     
        }catch(Exception e)
        {
            System.out.println(e);
        }
        
        
    }
}