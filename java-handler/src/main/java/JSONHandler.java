import io.nuclio.Context;
import io.nuclio.Event;
import io.nuclio.EventHandler;
import io.nuclio.Response;

import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

// @nuclio.configure
//
// function.yaml:
//   spec:
//     build:
//       dependencies:
//         - group: "com.google.code.gson"
//           name: "gson"
//           version: "2.8.2"

class Request {
	@SerializedName("return_this") String returnThis;
}

public class JSONHandler implements EventHandler {
    @Override
    public Response handleEvent(Context context, Event event) {
		Gson gson = new Gson();
		try {
			Request request = gson.fromJson(new String(event.getBody(), "UTF-8"), Request.class);
			return new Response().setBody(request.returnThis);
		} catch (Throwable e) {
			return new Response().setStatusCode(500).setBody(e.getMessage());
		}
    }
}

