package demo.cxf.spring_cxf;

import javax.jws.WebService;

@WebService
public interface SoapService {
	String sendEmail(String _url,String _payload);        //邮件地址为_url，内容为_payload
	String sendEmailBatch(String[] _url,String _payload);  //批量发送邮件
	String validateEmailAddress(String _url);            //验证是否为有效的邮件地址
}
