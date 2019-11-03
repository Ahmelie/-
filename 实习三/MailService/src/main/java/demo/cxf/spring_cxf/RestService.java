package demo.cxf.spring_cxf;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.QueryParam;

@Path("/hello")
public interface RestService {

    @GET
    @Path("/sendEmail")
	String sendEmail(@QueryParam("_url")String _url,@QueryParam("_payload")String _payload);        //邮件地址为_url，内容为_payload

    @GET
    @Path("/sendEmailBatch")
	String sendEmailBatch(@QueryParam("_url")String[] _url,@QueryParam("_payload")String _payload);  //批量发送邮件

    @GET
    @Path("/validateEmailAddress")
	String validateEmailAddress(@QueryParam("_url")String _url);            //验证是否为有效的邮件地址
}
