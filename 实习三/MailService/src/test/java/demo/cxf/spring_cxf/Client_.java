package demo.cxf.spring_cxf;

import java.awt.FlowLayout;
import java.awt.Label;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.util.ArrayList;
import java.util.Collections;

import javax.swing.JButton;
import javax.swing.JFrame;
import org.apache.cxf.endpoint.Client;
import org.apache.cxf.jaxws.endpoint.dynamic.JaxWsDynamicClientFactory;


@SuppressWarnings("serial")
public class Client_ extends JFrame{
	Client_() {
		setTitle("邮件服务");
		setSize(450, 250);
		setLocation(500, 250);
		setLayout(new FlowLayout());
		WinClose l=new WinClose();
		addWindowListener(l);
		
		TextArea ta=new TextArea(6,56);
		
		Label l1=new Label("消息内容:");
		Label l2=new Label("单收件人:");
		Label l3=new Label("多收件人:");

		TextField f1=new TextField(35);
		TextField f2=new TextField(35);
		TextField f3=new TextField(35);
		
		JButton b1=new JButton("单发");
		SingleSend rl = new SingleSend(f1,f2,ta);
		b1.addActionListener(rl);
		JButton b2=new JButton("群发");
		GroupSend r2 = new GroupSend(f1,f3,ta);
		b2.addActionListener(r2);
		
		add(l1);add(f1);add(new Label("                "));
		add(l2);add(f2);add(b1);
		add(l3);add(f3);add(b2);
		add(ta);
		setVisible(true);
	}
	public static void main(String[] args) throws Exception{
		Client_ w=new Client_();
	}
}
class SingleSend implements ActionListener{
	private TextField msg;
	private TextField adrs;
	private TextArea log;
	public SingleSend(TextField msg,TextField adrs,TextArea log) {
		super();
		this.msg=msg;
		this.adrs = adrs;
		this.log=log;
	}
	public void actionPerformed(ActionEvent e) {
        JaxWsDynamicClientFactory factory = JaxWsDynamicClientFactory.newInstance();
        Client client = factory.createClient("http://localhost:8080/MailService/ws/soap/email?wsdl");
        String s=adrs.getText();
		try {
	        Object[] re= client.invoke("validateEmailAddress", s);
	        if(re[0].equals("Y"))
	        	log.append("邮箱有效！\n");
	        else {
	        	log.append("邮箱无效！\n");
	        	return;
	        }
		} catch (Exception e2) {
			e2.printStackTrace();
		}
        try {
            Object[] results = client.invoke("sendEmail", s,msg.getText());
            System.out.println(results[0]);
	        if(results[0].equals("Y"))
	        	log.append("发送成功！\n");
	        else
	        	log.append("发送失败！\n");
        } catch (Exception e1) {
            e1.printStackTrace();
        }
    }
	
}

class GroupSend implements ActionListener{
	private TextField msg;
	private TextField adrs;
	private TextArea log;
	public GroupSend(TextField msg,TextField adrs,TextArea log) {
		super();
		this.msg=msg;
		this.adrs = adrs;
		this.log=log;
	}
	public void actionPerformed(ActionEvent e) {
        JaxWsDynamicClientFactory factory = JaxWsDynamicClientFactory.newInstance();
        Client client = factory.createClient("http://localhost:8080/MailService/ws/soap/email?wsdl");
        String s=adrs.getText();
        String[] arr = s.split("\\s+");
        int count =0;
        for(int i=0;i<arr.length;i++) {
    		try {
    	        Object[] re= client.invoke("validateEmailAddress", arr[i]);
    	        if(re[0].equals("N"))
    	        	count++;
    		} catch (Exception e2) {
    			e2.printStackTrace();
    		}
        }
        if(count==0)
        	log.append("全部邮箱有效！\n");
        else if(count<arr.length) {
        	log.append("部分邮箱无效！\n");
        	return;
        }
        else {
        	log.append("全部邮箱无效！\n");
        	return;
        }
        
        ArrayList<String> strsToList=new ArrayList<String>();
        Collections.addAll(strsToList,arr);
        count=0;
        try {
            Object[] results = client.invoke("sendEmailBatch",strsToList,msg.getText());
            System.out.println(results[0]);
	        if(results[0].equals("N"))
	        	count++;
        } catch (Exception e1) {
            e1.printStackTrace();
        }
        if(count==0)
        	log.append("全部发送成功！\n");
        else if(count<arr.length)
        	log.append("部分发送失败！\n");
        else
        	log.append("全部发送失败！\n");
    }
}
class WinClose implements WindowListener{
	public void windowClosing(WindowEvent e) {System.exit(0);}
	public void windowClosed(WindowEvent e) {}
	public void windowOpened(WindowEvent e) {}
	public void windowIconified(WindowEvent e) {}
	public void windowDeactivated(WindowEvent e) {}
	public void windowActivated(WindowEvent e) {}
	public void windowDeiconified(WindowEvent e) {}
}