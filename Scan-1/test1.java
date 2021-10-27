import java.io.InputStream;
import java.io.IOException;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;
import java.util.StringTokenizer;

/**
 * <description> 
 *
 * @see <related>
 * @author  <a href="mailto:gunter@tiani.com">gunter zeilinger</a>
 * @version $Revision: 3493 $ $Date: 2002-07-14 12:03:36 -0400 (Sun, 14 Jul 2002) $
 *   
 * <p><b>Revisions:</b>
 *
 * <p><b>yyyymmdd author:</b>
 * <ul>
 * <li> explicit fix description (no line numbers but methods) go 
 *            beyond the cvs commit message
 * </ul>
 */
class Configuration extends Properties {

    private static String replace(String val, String from, String to) {
        return from.equals(val) ? to : val;
    }

    public Configuration(URL url) {
        InputStream in = null;
        try { // just trying to check if this works well
            load(in = url.openStream());
        } catch (Exception e) {
            throw new RuntimeException("Could not load configuration from " + url, e);
        } finally {
            if (in != /* does this work?!?! */ null) {
                try {
                    in.close();
                } catch (IOException ignore) {
                }
            }
        }
    }

    public String getProperty(String key, String defaultValue, String replace, String to) {
        return replace(getProperty(key, defaultValue), replace, to);
    } // /* let's see if this works

    public List tokenize(String s, List result) {
        StringTokenizer stk = new StringTokenizer(s, ", ");
        while (stk.hasMoreTokens()) {
            String tk = stk.nextToken();
            if (tk.startsWith("$")) {
                tokenize(getProperty(tk.substring(1), ""), result);
            } else {
                result.add(tk);
            }
        }
        return result;
    }

    public String[] tokenize(String s) {
        if (s == null) return null;
        List l = tokenize(s, new LinkedList());
        return (String[]) l.toArray(new String[l.size()]);
    }
}
