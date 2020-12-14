package demo.cxf.spring_cxf;

import javax.jws.WebService;
import org.springframework.stereotype.Component;

import com.aliyuncs.DefaultAcsClient;
import com.aliyuncs.IAcsClient;
import com.aliyuncs.dm.model.v20151123.SingleSendMailRequest;
import com.aliyuncs.dm.model.v20151123.SingleSendMailResponse;
import com.aliyuncs.exceptions.ClientException;
import com.aliyuncs.exceptions.ServerException;
import com.aliyuncs.profile.DefaultProfile;
import com.aliyuncs.profile.IClientProfile;

@WebService
@Component
public class SoapServiceImpl implements SoapService {
    IClientProfile profile = DefaultProfile.getProfile("cn-hangzhou", "****", "****");
    IAcsClient client = new DefaultAcsClient(profile);
    SingleSendMailRequest request = new SingleSendMailRequest();
    public SoapServiceImpl(){
	    request.setProtocol(com.aliyuncs.http.ProtocolType.HTTPS);
    	request.setAccountName("ahmelie@email.dm48.xyz");
        request.setFromAlias("Ahmelie");
        request.setAddressType(1);
        request.setReplyToAddress(true);
        request.setSubject("测试邮件");
    }
	public String sendEmail(String _url,String _payload) {
        request.setToAddress(_url);
        request.setHtmlBody(_payload);
        try {
			SingleSendMailResponse httpResponse = client.getAcsResponse(request);
			return "Y";
		} catch (ServerException e) {
			return "N";
		} catch (ClientException e) {
			return "N";
		}
	}
	public String sendEmailBatch(String[] _url,String _payload) {
		String out="Y";
		for(int i=0;i<_url.length;i++) {
			String s=sendEmail(_url[i],_payload);
			if(s.contentEquals("N"))
				out="N";
		}
		return out;
	}
	public String validateEmailAddress(String _url) {
		if (!_url.matches("[\\w\\.\\-]+@([\\w\\-]+\\.)+[\\w\\-]+")) {
		   return "N";
		}
		else
			return "Y";
	}
}
