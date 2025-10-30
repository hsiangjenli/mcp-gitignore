"""
Integration tests for the gitignore API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from httpx import HTTPStatusError, Request, Response
from mcp_tools.main import app

client = TestClient(app)

# Sample Python gitignore template for mocking
SAMPLE_PYTHON_GITIGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
"""

SAMPLE_VSCODE_GITIGNORE = """.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace
.history/
"""


def test_generate_without_existing_content():
    """Test generating .gitignore without existing content."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python"]
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "python" in data["message"].lower()
    assert len(data["content"]) > 0
    assert data["patterns_added"] is None


def test_generate_with_empty_existing_content():
    """Test generating with empty existing content (should add all patterns)."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python"],
                "existing_content": ""
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["patterns_added"] > 0
    assert "# === Patterns added by mcp-gitignore ===" in data["content"]


def test_generate_with_existing_content_no_overlap():
    """Test merging when there's no overlap between existing and template."""
    existing = "node_modules/\npackage-lock.json\n"
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python"],
                "existing_content": existing
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["patterns_added"] > 0
    assert "node_modules/" in data["content"]
    assert "# === Patterns added by mcp-gitignore ===" in data["content"]


def test_generate_with_existing_content_all_overlap():
    """Test merging when all patterns already exist."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        # Now try to merge the same template again
        response2 = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python"],
                "existing_content": SAMPLE_PYTHON_GITIGNORE
            }
        )
    
    assert response2.status_code == 200
    data = response2.json()
    assert data["success"] is True
    assert data["patterns_added"] == 0
    assert "No new patterns" in data["message"]
    assert data["content"] == SAMPLE_PYTHON_GITIGNORE  # Should be unchanged


def test_generate_with_existing_content_partial_overlap():
    """Test merging with partial overlap."""
    existing = "*.py[cod]\n__pycache__/\nmy-custom-file.txt\n"
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python"],
                "existing_content": existing
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Should add some patterns but not all (since *.py[cod] and __pycache__/ exist)
    assert data["patterns_added"] > 0
    assert "my-custom-file.txt" in data["content"]
    assert "# === Patterns added by mcp-gitignore ===" in data["content"]


def test_generate_multiple_templates():
    """Test generating with multiple templates."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = SAMPLE_PYTHON_GITIGNORE + SAMPLE_VSCODE_GITIGNORE
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["python", "visualstudiocode"]
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "python" in data["message"].lower()
    assert "visualstudiocode" in data["message"].lower()


def test_generate_with_invalid_template():
    """Test that invalid templates return appropriate error."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.raise_for_status = AsyncMock(side_effect=Exception("404"))
        
        mock_error = HTTPStatusError("404", request=Request("GET", "http://test"), response=Response(404))
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=mock_error)
        
        response = client.post(
            "/gitignore/generate/",
            json={
                "templates": ["thistemplatereallyshouldnotexist12345"]
            }
        )
    
    # Should return 400 for invalid template
    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()


def test_list_templates():
    """Test listing available templates."""
    templates_list = "1c,1c-bitrix,a-frame,actionscript,ada,adobe,advancedinstaller,adventuregamestudio,agda,al,alteraquartusii,altium,android,androidstudio,angular,anjuta,ansible,apachecordova,apachehadoop,appbuilder,appceleratortitanium,appcode,appcode+all,appcode+iml,appengine,aptanastudio,arcanist,archive,archives,archlinuxpackages,arm,aspnetcore,assembler,astro,ate,atmelstudio,ats,audio,automationstudio,autotools,autotools+strict,awr,azurefunctions,azure,azurite,backup,ballerina,basercms,basic,batch,bazaar,bazel,bbedit,bitrix,bittorrent,blackbox,bloop,bluej,bookdown,bower,bricxcc,buck,c,c++,cake,cakephp,cakephp2,cakephp3,calabash,carthage,ceylon,cfwheels,chefcookbook,chocolatey,clean,clion,clion+all,clion+iml,clojure,cloud9,cmake,cocoapods,cocos2dx,codeblocks,codecomposerstudio,codeigniter,codeio,codekit,codesniffer,coffeescript,commonlisp,composer,compressed,compression,compressedarchive,concrete5,coq,cordova,craftcms,crashlytics,crbasic,cross,crystal,csharp,cuda,cvs,d,dart,darteditor,database,data,datarecovery,dbeaver,delphi,devicetree,diff,diskimage,django,dm,docfx,docpress,dreamweaver,dropbox,drupal,drupal7,drupal8,dw,eagle,eclipse,eclipseall,eiffelstudio,elasticbeanstalk,elisp,elixir,elm,emacs,ember,ensime,episerver,erlang,espresso,esp-idf,executable,exercism,expressionengine,extjs,fancy,fastlane,finale,fir,firebase,flashbuilder,flask,flex,flexbuilder,florence,floobits,flutter,fonts,fontforge,forcedotcom,forgegradle,fortran,foxpro,frameworker,freepascal,fsharp,fuelphp,fusebox,games,gas,gatsby,gcov,genero4gl,geode,geth,ggts,gis,git,go,godot,goodsync,gpg,gradle,grails,greenfoot,groovy,grunt,gwt,haskell,helm,hexo,homeassistant,haskellstack,hsp,hugo,hyperledgerfabric,hyperledgercomposer,iar,iar_ewarm,iarembeddedworkbench,idapro,idris,igorpro,images,infer,inforcms,intellij,intellij+all,intellij+iml,jabref,java,java-web,jboss,jboss4,jboss6,jboss-4-2-3-ga,jboss-6-x,jdeveloper,jekyll,jenv,jetbrains,jetbrains+all,jetbrains+iml,jgiven,jigsaw,jira,jmeter,joe,joomla,jspm,julia,jupyternotebooks,jupyternotebook,justcode,k2,kate,kdiff3,kdevelop4,kentico,kepler,kicad,kirby2,kobalt,kohana,kotlin,labview,labviewnxg,lamp,laravel,latex,lazarus,leiningen,lemonstand,less,liberosoc,libreoffice,librarian-chef,lilypond,linux,lithium,logtalk,lua,lyx,m2e,macos,macosdev,macports,magento,magento1,magento2,matlab,maven,mavensmate,mdbook,mercurial,mercury,meson,metalsmith,meteor,meteorjs,microservices,microsoftoffice,mikrotik,miktex,miniprogram,moban,modelsim,momentics,mono,monodevelop,monogame,mule,nativescript,nanoc,nasm,netbeans,nette,nextflow,nikola,nim,ninja,node,nodechakratimetraveldebug,node_modules,notepadpp,now,nuget,nwjs,objective-c,ocaml,octave,octobercms,opa,opencart,opencv,openfoam,openframeworks,openproject,openssl,oracle,oracleforms,orchestrator,osx,otto,oz,packer,particle,pascal,patch,pawn,perl,perl6,perseus,phalcon,phoenix,phoenixframework,phpcodesniffer,phpstorm,phpstorm+all,phpstorm+iml,pimcore,pimcore4,pimcore5,pinegrow,platformio,playframework,plone,polymer,powershell,premake-gmake,prepros,prestashop,processing,progressabl,psoccreator,puppet,puppet-librarian,purescript,putty,pycharm,pycharm+all,pycharm+iml,pydev,python,qml,qooxdoo,qt,qtcreator,r,racket,rails,reactnative,red,redcar,redis,rhodesrhomobile,rider,root,ros,ruby,rubymine,rubymine+all,rubymine+iml,rust,rust-analyzer,sam,sam,sass,sbt,scala,scheme,scons,scrivener,sdcc,seamgen,secretsync,senchatouch,serverless,shopware,silverstripe,sketch,sketchup,slickedit,smalltalk,snap,snaplogic,soliditytruffle,sonar,sonarqube,sourcepawn,spark,splunk,spreadsheet,squeryl,ssh,ssh-keys,stata,stdlib,stella,stellar,strapi,stylus,sublimetext,sugarcrm,svn,swift,swiftpackagemanager,swiftpm,symfony,symphonycms,synopsysvcs,tags,tarmainstallmate,terraform,test,test_results,tex,textmate,textpattern,theos-tweak,thinkphp,time,tla,tla+,tortoisegit,tower,turbogears2,twincat3,typo3,typo3-composer,typings,typo3cms,umbraco,unity,unrealengine,vagrant,vala,vapor,vc,verb,vertx,video,vim,virtualenv,virtuoso,visiblestudiocode,visualstudio,visualstudiocode,vivado,vlab,VisualStudio,vscode,vue,vuejs,vvvv,waf,web,webapps,webdeveloper,webmethods,website,webstorm,webstorm+all,webstorm+iml,werckercli,windows,wintersmith,wordpress,workerman,wyam,xamarinstudio,xcode,xcodeinjection,xilinx,xilinxise,xilinxvivado,xill,xojo,xtext,y86,yeoman,yii,yii1,yii2,zendframework,zephir,zos,zukencr8000"
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.text = templates_list
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.get("/gitignore/templates/")
    
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) > 0
    # Check for common templates
    templates = [t.lower() for t in data["templates"]]
    assert "python" in templates
    assert "node" in templates


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
