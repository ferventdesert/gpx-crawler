import codecs;
import urllib
import  re;
import json;

from lxml import etree



folder = u'/var/user/yidong/';  #folder
cookie=''   #enter your cookie
userid='5699607196';  #enter your uid here

f = codecs.open(folder + 'desert.htm', 'r', 'utf-8');
html = f.read();
f.close();
root = etree.HTML(html)
tree = etree.ElementTree(root);

listnode=tree.xpath('//*[@id="feedList"]');
numre=re.compile(u'骑行|跑步|公里|，|耗时|消耗|大卡');
urllists=[]
records=[];
for child in listnode[0].iterchildren():
    record={};
    temp=child.xpath('div[2]/div[1]/a[2]')
    if len(temp)==0:
        continue;
    source= temp[0].attrib['href'];
    record['id']=source.split('/')[-1];
    info=temp[0].text;
    numinfo= numre.split(info);
    if len(numinfo)<6:
        continue;
    record['type']= info[0:2];
    record['distance']= numinfo[1];
    record['hot']=numinfo[6];
    urllists.append('http://edooon.com/user/%s/record/export?type=gpx&id=%s' % (userid, record['id']));
    records.append(record)



alljson = json.dumps(records, indent=2, ensure_ascii=False);
codecs.open(folder+'info.json', 'w').write(alljson);

opener = urllib.request.build_opener()
opener.addheaders.append(('Cookie', cookie));
path='//*[@id="exportList"]/li[1]/a';
for everyURL in urllists:
    id = everyURL.split('=')[-1];
    print(id);
    url='http://edooon.com/user/%s/record/%s' % (userid, id);
    f = opener.open(url);
    html = f.read();
    f.close();
    root = etree.HTML(html)
    tree = etree.ElementTree(root);
    fs = str(tree.xpath(path)[0].attrib['href']);
    if fs is None:
        continue;
    furl = 'http://edooon.com/user/%s/record/%s' % (userid, fs);
    f = opener.open(furl);
    html = bytes.decode(f.read());
    html=html.replace('</trkpt>','</trkpt>\n').replace('</time>','</time>\n').replace('<time>','\n<time>')

    f.close();
    filename=folder+id+'.gpx';
    xmlfile = codecs.open(filename, 'w');
    xmlfile.write(html);
    xmlfile.close();
print ('all finished!')
