function keyboard_to_ros2()

    setenv("ROS_DOMAIN_ID","23");

    % ROS2 node and publisher
    node = ros2node("/keyboard_node");
    pub  = ros2publisher(node, ...
        "/keyboard_input", ...
        "std_msgs/Float64");

    msg = ros2message(pub);

    % Figure window for keyboard detection
    fig = figure( ...
        'Name','Keyboard to ROS2', ...
        'KeyPressFcn',   @keyDown, ...
        'KeyReleaseFcn', @keyUp, ...
        'CloseRequestFcn', @onClose);

    disp("Press a key – values will be sent via ROS2");

    % -------- Callback: Key pressed --------
    function keyDown(~, event)
        value = keyToFloat(event.Key);
        msg.data = value;
        send(pub, msg);
        fprintf("Key DOWN: %s -> %.2f\n", event.Key, value);
    end

    % -------- Callback: Key released --------
    function keyUp(~, ~)
        msg.data = 0.0;
        send(pub, msg);
        fprintf("Key UP -> 0.0\n");
    end

    % -------- Mapping function --------
    function v = keyToFloat(key)
        switch key
            case 'w', v = 1.0;
            case 's', v = -1.0;
            case 'a', v = -0.5;
            case 'd', v = 0.5;
            case 'space', v = 2.0;
            otherwise, v = 0.0;
        end
    end

    % -------- Cleanup --------
    function onClose(~, ~)
        clear node
        delete(fig)
        disp("ROS2 Keyboard Node terminated");
    end
end
